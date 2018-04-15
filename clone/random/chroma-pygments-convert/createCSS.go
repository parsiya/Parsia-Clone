package main

import (
	"os"

	"github.com/alecthomas/chroma/formatters/html"
	"github.com/alecthomas/chroma/styles"
)

func main() {
	f, _ := os.Create("solarized-dark.css")
	defer f.Close()

	formatter := html.New(html.WithClasses(), html.WithLineNumbers())
	if err := formatter.WriteCSS(f, styles.Get("solarized-dark")); err != nil {
		panic(err)
	}
}
