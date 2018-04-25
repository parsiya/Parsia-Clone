package styles

import (
	"github.com/alecthomas/chroma"
)

// SolarizedDark style.
var SolarizedDark = Register(chroma.MustNewStyle("solarized-dark", chroma.StyleEntries{
	chroma.GenericEmph:           "italic",
	chroma.Keyword:               "#719e07",
	chroma.GenericError:          "#DC322F bold",
	chroma.GenericHeading:        "#CB4B16",
	chroma.GenericDeleted:        "#DC322F",
	chroma.CommentSpecial:        "#719e07",
	chroma.NameConstant:          "#CB4B16",
	chroma.Operator:              "#719e07",
	chroma.KeywordConstant:       "#CB4B16",
	chroma.LiteralStringChar:     "#2AA198",
	chroma.LiteralNumber:         "#2AA198",
	chroma.NameAttribute:         "#93A1A1",
	chroma.LiteralStringDoc:      "#93A1A1",
	chroma.KeywordDeclaration:    "#268BD2",
	chroma.LiteralStringRegex:    "#DC322F",
	chroma.NameException:         "#CB4B16",
	chroma.NameBuiltinPseudo:     "#268BD2",
	chroma.NameVariable:          "#268BD2",
	chroma.LiteralString:         "#2AA198",
	chroma.LiteralStringHeredoc:  "#93A1A1",
	chroma.NameClass:             "#268BD2",
	chroma.CommentPreproc:        "#719e07",
	chroma.NameFunction:          "#268BD2",
	chroma.Background:            "#93A1A1 bg:#002B36",
	chroma.LiteralStringBacktick: "#586E75",
	chroma.GenericInserted:       "#719e07",
	chroma.NameEntity:            "#CB4B16",
	chroma.GenericStrong:         "bold",
	chroma.NameDecorator:         "#268BD2",
	chroma.Comment:               "#586E75",
	chroma.KeywordType:           "#DC322F",
	chroma.LiteralStringEscape:   "#CB4B16",
	chroma.NameBuiltin:           "#B58900",
	chroma.Other:                 "#CB4B16",
	chroma.GenericSubheading:     "#268BD2",
	chroma.NameTag:               "#268BD2",
	chroma.KeywordReserved:       "#268BD2",
}))
