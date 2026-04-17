// ---------------------------------------------------------------------------
// headingJoin: Controls blank lines after headings.
// Returns 0 (no blank line) between a heading and a paragraph, UNLESS the
// paragraph is actually a table (without remark-gfm, tables are paragraph
// nodes). Returns 1 (single blank line) for all other sibling types.
// ---------------------------------------------------------------------------
function headingJoin(left, right) {
  if (left.type === 'heading') {
    if (right.type === 'paragraph' && !looksLikeTable(right)) return 0
    return 1
  }
}

// ---------------------------------------------------------------------------
// looksLikeTable: Helper for headingJoin. Without remark-gfm, tables are
// parsed as paragraph nodes. This reconstructs the raw text from a
// paragraph's children and checks if the second line is a table delimiter
// row (e.g., |---|---|).
// ---------------------------------------------------------------------------
function looksLikeTable(node) {
  if (!node.children) return false
  // Reconstruct raw text including backtick-wrapped inline code
  const raw = node.children.map(c => {
    if (c.type === 'text') return c.value
    if (c.type === 'inlineCode') return '`' + c.value + '`'
    return ''
  }).join('')
  const lines = raw.split('\n')
  if (lines.length < 2) return false
  // Check if the second line is a delimiter row (all cells are dashes with
  // optional colons for alignment)
  const cells = parseCells(lines[1])
  return cells.length > 0 && cells.every(c => /^:?-+:?$/.test(c))
}

// ---------------------------------------------------------------------------
// formatTables: Compiler wrapper that pads table columns to equal width.
// Wraps self.compiler (own property) to post-process the serialized markdown.
// Cannot use an AST transformer because without remark-gfm, tables are not
// parsed into table/tableRow/tableCell nodes — they're paragraph > text.
// ---------------------------------------------------------------------------
function formatTables() {
  const self = this
  const orig = self.compiler
  self.compiler = function(tree, file) {
    const result = orig.call(this, tree, file)
    // Match table blocks: header row, delimiter row, and data rows
    return result.replace(
      /^(\|[^\n]+\n\|[\s:|\-]+\n(?:\|[^\n]+\n?)*)/gm,
      (match) => formatTableText(match)
    )
  }
}

// Formats a single table: pads all cells to the widest value in each column.
function formatTableText(tableText) {
  const lines = tableText.trimEnd().split('\n')
  const rows = lines.map(parseCells)
  const colCount = Math.max(...rows.map(r => r.length))

  // Calculate max width per column (skip delimiter row at index 1)
  const colWidths = new Array(colCount).fill(0)
  for (let r = 0; r < rows.length; r++) {
    if (r === 1) continue
    for (let c = 0; c < rows[r].length; c++) {
      colWidths[c] = Math.max(colWidths[c], rows[r][c].length)
    }
  }
  // Minimum 3 chars per column (for delimiter dashes like ---)
  for (let c = 0; c < colCount; c++) {
    colWidths[c] = Math.max(colWidths[c], 3)
  }

  // Rebuild each row with padded cells
  return rows.map((cells, r) => {
    const padded = []
    for (let c = 0; c < colCount; c++) {
      const cell = cells[c] || ''
      if (r === 1) {
        // Delimiter row: rebuild with correct dash count, preserve alignment
        padded.push(buildDelimCell(cell, colWidths[c]))
      } else {
        // Content row: pad with trailing spaces
        padded.push(cell + ' '.repeat(colWidths[c] - cell.length))
      }
    }
    return '| ' + padded.join(' | ') + ' |'
  }).join('\n') + '\n'
}

// Splits a table row into trimmed cell values, stripping outer pipes.
function parseCells(line) {
  let s = line.trim()
  if (s.startsWith('|')) s = s.slice(1)
  if (s.endsWith('|')) s = s.slice(0, -1)
  return s.split('|').map(c => c.trim())
}

// Builds a delimiter cell (e.g., :---:) padded to the given width.
// Preserves colon alignment markers on left/right.
function buildDelimCell(cell, width) {
  const left = cell.startsWith(':')
  const right = cell.endsWith(':')
  const innerWidth = width - (left ? 1 : 0) - (right ? 1 : 0)
  return (left ? ':' : '') + '-'.repeat(innerWidth) + (right ? ':' : '')
}

// ---------------------------------------------------------------------------
// preserveFrontmatter: Parser + compiler wrapper that preserves YAML
// frontmatter (---...---). Without remark-frontmatter (npm package), remark
// parses --- as thematicBreak (***) and YAML lists as markdown lists,
// destroying frontmatter. This strips it before parsing and re-adds it after.
//
// Wraps self.parser and self.compiler (own properties on the processor).
// Must use own properties, NOT prototype methods (self.parse/self.stringify),
// because vscode-remark's language server copies own properties but not
// prototype overrides when cloning the processor.
//
// Must be FIRST in the plugins array so its compiler wrapper is outermost
// (runs last, after formatTables etc.).
// ---------------------------------------------------------------------------
function preserveFrontmatter() {
  const self = this
  const origParser = self.parser
  let savedFrontmatter = null

  // Wrap the parser: strip frontmatter before remark sees the document.
  self.parser = function(doc, file) {
    const str = String(doc)
    const match = str.match(/^---\n([\s\S]*?)\n---\n/)
    if (match) {
      savedFrontmatter = match[0]
      // Feed remark only the content after frontmatter
      return origParser(str.slice(match[0].length), file)
    }
    savedFrontmatter = null
    return origParser(doc, file)
  }

  // Wrap the compiler: prepend saved frontmatter to the serialized output.
  const origCompiler = self.compiler
  self.compiler = function(tree, file) {
    const result = origCompiler.call(this, tree, file)
    // Extra '\n' ensures a blank line between frontmatter closing --- and
    // the first content block. The saved frontmatter already ends with \n
    // (from the ---\n in the regex), so adding one more produces the blank line.
    return savedFrontmatter ? savedFrontmatter + '\n' + result : result
  }
}

// ---------------------------------------------------------------------------
// Custom handlers to disable remark-stringify's defensive escaping.
//
// remark-stringify calls state.safe() on text content and URLs, which escapes
// ~20 ASCII punctuation characters to prevent them from being reinterpreted
// as markdown syntax. This is safe to disable because remark already parsed
// real syntax (links, emphasis, etc.) into their own AST nodes — text nodes
// and URL properties contain only literal values.
//
// Three handlers cover all escaping:
//   text       — plain text content (skips state.safe())
//   link       — inline link URLs [text](url) (skips state.safe() for URL)
//   definition — reference definitions [label]: url (skips state.safe() for URL)
// ---------------------------------------------------------------------------
function textHandler(node) {
  return node.value
}

function linkHandler(node, _, state, info) {
  const exit = state.enter('link')
  const subexit = state.enter('label')
  const tracker = state.createTracker(info)
  let value = tracker.move('[')
  value += tracker.move(
    state.containerPhrasing(node, {
      before: value,
      after: '](',
      ...tracker.current()
    })
  )
  value += tracker.move('](')
  subexit()
  // Output URL directly — no state.safe()
  value += tracker.move(node.url || '')
  if (node.title) {
    value += tracker.move(' "' + node.title + '"')
  }
  value += tracker.move(')')
  exit()
  return value
}

function definitionHandler(node, _, state) {
  const exit = state.enter('definition')
  const subexit = state.enter('label')
  const id = state.associationId(node)
  subexit()
  let value = '[' + id + ']: ' + (node.url || '')
  if (node.title) {
    value += ' "' + node.title + '"'
  }
  exit()
  return value
}

// ---------------------------------------------------------------------------
// Export config
// ---------------------------------------------------------------------------
export default {
  settings: {
    bullet: '*',              // Use * for unordered list markers
    listItemIndent: 'one',     // Single space after list marker
    tightDefinitions: true,    // No blank lines between reference link definitions
    join: [headingJoin],       // Custom blank line control after headings
    handlers: {
      text: textHandler,
      link: linkHandler,
      definition: definitionHandler
    }
  },
  plugins: [
    preserveFrontmatter,                  // Must be first (outermost wrapper)
    formatTables                          // Align table columns
  ]
}
