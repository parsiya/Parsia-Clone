package styles

import (
	"github.com/alecthomas/chroma"
)

// SolarizedDark256 style.
var SolarizedDark256 = Register(chroma.MustNewStyle("solarized-dark256", chroma.StyleEntries{
	chroma.GenericError:          "#af0000 bold",
	chroma.OperatorWord:          "#5f8700",
	chroma.KeywordReserved:       "#0087ff",
	chroma.LiteralStringEscape:   "#af0000",
	chroma.NameDecorator:         "#0087ff",
	chroma.NameAttribute:         "#8a8a8a",
	chroma.Operator:              "#8a8a8a",
	chroma.NameConstant:          "#d75f00",
	chroma.NameTag:               "#0087ff",
	chroma.KeywordNamespace:      "#d75f00",
	chroma.NameException:         "#af8700",
	chroma.NameVariable:          "#0087ff",
	chroma.NameBuiltinPseudo:     "#0087ff",
	chroma.NameEntity:            "#d75f00",
	chroma.LiteralStringChar:     "#00afaf",
	chroma.LiteralNumber:         "#00afaf",
	chroma.Keyword:               "#5f8700",
	chroma.LiteralStringDoc:      "#00afaf",
	chroma.CommentSpecial:        "#5f8700",
	chroma.Background:            "#8a8a8a bg:#1c1c1c",
	chroma.GenericSubheading:     "#0087ff",
	chroma.LiteralStringRegex:    "#af0000",
	chroma.KeywordType:           "#af0000",
	chroma.NameBuiltin:           "#0087ff",
	chroma.GenericEmph:           "italic",
	chroma.NameFunction:          "#0087ff",
	chroma.GenericInserted:       "#5f8700",
	chroma.NameClass:             "#0087ff",
	chroma.LiteralString:         "#00afaf",
	chroma.Other:                 "#d75f00",
	chroma.LiteralStringBacktick: "#4e4e4e",
	chroma.GenericStrong:         "bold",
	chroma.CommentPreproc:        "#5f8700",
	chroma.KeywordConstant:       "#d75f00",
	chroma.GenericHeading:        "#d75f00",
	chroma.KeywordDeclaration:    "#0087ff",
	chroma.Comment:               "#4e4e4e",
	chroma.GenericDeleted:        "#af0000",
	chroma.LiteralStringHeredoc:  "#00afaf",
}))
