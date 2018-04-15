package styles

import (
	"github.com/alecthomas/chroma"
)

// Solarized style.
var Solarized = Register(chroma.MustNewStyle("solarized-light", chroma.StyleEntries{
	chroma.KeywordConstant:  "bold",
	chroma.Comment:          "#93a1a1 italic",
	chroma.KeywordNamespace: "#dc322f bold",
	chroma.Text:             "bg: #eee8d5 #586e75",
	chroma.Generic:          "#d33682",
	chroma.Name:             "#268bd2",
	chroma.NameTag:          "bold",
	chroma.Background:       " bg:#eee8d5",
	chroma.NameBuiltin:      "#cb4b16",
	chroma.LiteralNumber:    "bold",
	chroma.NameClass:        "#cb4b16",
	chroma.KeywordType:      "bold",
	chroma.Literal:          "#2aa198",
	chroma.Keyword:          "#859900",
	chroma.OperatorWord:     "#859900",
}))
