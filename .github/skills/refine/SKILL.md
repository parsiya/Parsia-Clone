---
name: refine
description: "Proofread Markdown without changing structure or voice. Use when editing or writing new material. to fix punctuation, typos, misspellings, grammar, and similar errors while preserving headings, bullets, links, frontmatter, formatting, and the author's style."
argument-hint: "Describe what to proofread, or run it on the current selection or file"
user-invocable: true
---

# Refine
Fix punctuation, typos, misspellings, grammar, and similar surface-level issues in Markdown.

## Constraints

- Preserve the author's voice.
- Preserve the existing structure.
- Keep edits scoped to what the user asked to change.
- Do not rewrite for style unless the original wording is clearly broken.
- Follow the repository Markdown instructions.

## Procedure

1. Fix surface-level errors first.
2. Make the smallest set of edits needed.
