# Converting Pygments Styles to Chroma
[Chroma][chroma] is a syntax highlighter written in Go. [Hugo][hugo-website] uses it for internal highlighting. My theme [Hugo-Octopress][hugo-octopress-github] used the [solarized dark][solarized-dark-github] theme built into the CSS (from Octopress). Chroma does not support this theme, so I had to generate the CSS myself.

Chroma has a [built-in tool for converting styles][chroma-styles] `_tools/style.py`.

## Instructions
These are for an Ubuntu 16 machine, but can be adapted for any OS.

1. Install Go.
2. Install Chroma with `https://github.com/alecthomas/chroma`.
3. Install Python 3.
4. Install Pygments for Python 3: `sudo apt-get install python3-pygments`.
5. Install Pystache for Python 3: `sudo apt-get install python3-pystache`.
5. Clone `solarized dark`: `git clone https://github.com/john2x/solarized-pygment/` (do not need to install it).
6. (Optional) Rename the three py files inside `solarized=pygment/pygments_solarized` to more descriptive names. For example `dark.py` might become `solarized-dark.py`.
7. Open each of them and note the class name. For example for `dark.py` it's `SolarizedDarkStyle`.
8. Copy the files to the `pygments` installation path. On my machine it was:
    * `/usr/local/lib/python3.5/dist-packages/Pygments-2.2.0-py3.5.egg/pygments/styles`.
9. Use the `_tools/style.py` to generate `go` files from styles:
    * `python3 style.py [style-name] pygments.styles.[py-file-name].[style-class-name] > style-name.go`
        - `style-name` is a string with new style's name. E.g. `solarized-dark`.
        - `py-file-name` is the name of the `py` file (w/o extension) that was copied to pygments. E.g. `dark`.
        - `style-class-name` is the name of the python class inside the style. E.g. `SolarizedDarkStyle`.
10. My example command was:
    *  `python3 style.py solarized-dark pygments.styles.dark.SolarizedDarkStyle > solarized-dark.go`
11. Repeat for any other styles.
12. Copy the resulting `go` files to `$GOPATH/Go/src/github.com/alecthomas/chroma/styles`.
    * You can open the file to double-check the style name passed to `chroma.MustNewStyle`:
    * `var SolarizedDark = Register(chroma.MustNewStyle("solarized-dark", chroma.StyleEntries{`
13. Now create the following Go application (or copy `createCSS.go`). Modify the file and style names as needed:
    ``` go
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
    ```
14. Your CSS file is now ready.


<!-- Links -->

[chroma]: https://github.com/alecthomas/chroma
[hugo-website]: https://gohugo.io/
[hugo-octopress-github]: https://github.com/parsiya/Hugo-Octopress
[solarized-dark-github]: https://github.com/john2x/solarized-pygment/
[chroma-styles]: https://github.com/alecthomas/chroma#styles