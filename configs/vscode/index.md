---
title: "VS Code Config"
draft: false
toc: false
comments: false
categories:
- Configs
tags:
- VS Code
wip: false
snippet: "My config files for Visual Studio Code."

---

# VS Code Config <!-- omit in toc -->
This is how I setup my VS Code. I mostly use it for reading/writing markdown and Go.

- [Quick Start Guide](#quick-start-guide)
- [Extensions](#extensions)
    - [Go](#go)
        - [golangci-lint](#golangci-lint)
        - [Go Snippets](#go-snippets)
    - [Markdown All in One](#markdown-all-in-one)
        - [Table of Content](#table-of-content)
    - [MarkdownLint](#markdownlint)
    - [GitLens](#gitlens)
    - [LanguageTool for Visual Studio Code](#languagetool-for-visual-studio-code)
    - [Code Spell Checker](#code-spell-checker)
- [General Settings](#general-settings)
    - [Disable git](#disable-git)
    - [Markdown Settings](#markdown-settings)
        - [Word Separator Note](#word-separator-note)
- [Creating Snippets](#creating-snippets)

**Note:** This guide was originally made in early 2019. Some of the options and
extensions have changed since then. For example, gometalinter is not supported
anymore. I have not updated the guide, yet. Keep that in mind when reading this
document. The `settings.json` is always updated, regardless.

# Quick Start Guide

1. Install Go. I mostly code in Go these days, so that's a step.
2. Download and install VS Code (optionally install Git when VS Code asks).
3. Copy paste the `settings.json` from the [Github repository](https://github.com/parsiya/Parsia-Clone/tree/main/configs/vscode/vs-code-config-files/settings.json) (or [here](vs-code-config-files/settings.json)) to user config (shortcut `ctrl + ,`).
4. Install `Go` extension and reload.
5. Open any file with `go` extension. When prompted, select `Install All`. Wait until all tools are installed.
6. Optionally install the `Markdown All in One` extension and reload.
7. Now intellisense should work for Go and Markdown.

# Extensions
Some useful extensions.

## Go

- Docs: https://code.visualstudio.com/docs/languages/go
- Source: https://github.com/Microsoft/vscode-go

### golangci-lint
To enable [golangci-lint](https://github.com/golangci/golangci-lint) set the following in config:

``` json
    "go.lintTool": "golangci-lint",
    // Lint all workspace, this is good for source code review
    // Other options are "off" or "package"
    "go.lintOnSave": "workspace",
```

Then run `go get -v github.com/golangci/golangci-lint/cmd/golangci-lint`.

Next, open up any Go file and the extension will prompt you to install tools.
Select all and tools will be installed.

### Go Snippets
Go extension comes with some snippets. These snippets are at:

- https://github.com/golang/vscode-go/blob/master/snippets/go.json

## Markdown All in One
Helps with editing markdown.

- https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one

``` json
    // Generate Github compatible table of content
    "markdown.extension.toc.slugifyMode": "github",
    // Update the table of content on save
    "markdown.extension.toc.updateOnSave": true,
    // Set list indentation to inherit
    "markdown.extension.list.indentationSize": "inherit",
    // Convert toc to lowercase to work on Github and Hugo
    "markdown.extension.toc.downcaseLink": true,
    // Use '*' to indicate italic and not '_'
    "markdown.extension.italic.indicator": "*",
```

### Table of Content
Add the initial table of content: Press `ctrl+shift+p` and type `ctoc` in the
palette.

To ignore a heading and all its subheadings, add `<!-- omit in toc -->` at the
end of the heading. This is useful for eliminating the top-level Github heading.
Just be sure that the rest of your headings are not subheadings for the top one
(e.g. if top heading is `h1`, next heading should also be `h1`). In this
document I have ignored the top heading `VS Code Config`.

## MarkdownLint
Linter for markdown.

- https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint

You can disable specific rules in config:

``` json
    // Markdown Lint settings
    "markdownlint.config": {
        // Disable some rules
        "MD022": false,
        "MD032": false,
        "MD007": false,
        "MD010": false,
    },
```

## GitLens
Adds Git Integration.

- https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens

I have disabled some clutter:

``` json
    "gitlens.codeLens.recentChange.enabled": false,
    "gitlens.codeLens.authors.enabled": false,
    "gitlens.historyExplorer.enabled": false,
```

## LanguageTool for Visual Studio Code
This extension enables some grammar and spelling rules.

- https://marketplace.visualstudio.com/items?itemName=adamvoss.vscode-languagetool

You must also install specific language supports. E.g. English:

- https://marketplace.visualstudio.com/items?itemName=adamvoss.vscode-languagetool-en

## Code Spell Checker
Enables spell check. You can add new words to it (they will be stored in user
settings file):

- https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker

# General Settings
Press `ctrl + ,` to open the config file. It supports intellisense/suggestions.

## Disable git
Helps with performance inside VMs where I do not need git integration.

``` json
{
    "git.enabled": false,
    "git.path": null,
    "git.autofetch": false,
}
```

## Markdown Settings
These settings only affect markdown files. VS Code has a recent bug where some
universal settings (e.g. `quickSuggestions`) are not automatically applied to
some languages such as Markdown. These are added here.

``` json
    // Markdown language settings
    "[markdown]": {
        // Enable word based suggestions
        "editor.wordBasedSuggestions": true,
        // Disable drag and drop in markdown files
        "editor.dragAndDrop": false,
        // Enable quick suggestions
        "editor.quickSuggestions": true,
        // Send snippets to top in suggestion list
        "editor.snippetSuggestions": "top",
    },
```

### Word Separator Note
Unlike Sublime, VS Code counts `-` as word separator. In VS Code this is called
`word pattern`. This means you will not get suggestions for `this-long-word`.
The `editor.wordSeparators` config setting does not have any effect on word
patterns:

``` json
    // "editor.wordSeparators" does not affect word pattern :(
    // Note I have removed -
    // "editor.wordSeparators": "`~!@#$%^&*()=+[{]}\\|;:'\",.<>/?",
```

# Creating Snippets
Similar to other editors, you can create snippets in VS Code. Snippets are
stored in JSON files. To create a snippet for a specific language use `File
(menu) > Preferences > User Snippets`. Then select the language. In this case, I
will create some Markdown snippets, so I will select `markdown.json`.

The JSON object is easy to read. The important parts are `prefix` (which is the
trigger) and `body`. Note that you do not need to enter new lines with `\n`.
Simply create a new cell in the body array and it will be printed in a new line.
The following snippet will create a codefence.

``` json
{
	"codefence": {
		"prefix": "ffe",
		"body": [
			"``` ${1:language}",
			"${2:code}",
			"```",
			"",
			"$0"
		],
		"description": "Markdown codefence"
    },
}
```

`${1:language}` means:

- It's the first place where your cursor is after the snippet is activated.
- The default text is `language`.

After pressing tab, cursor will go to `$2` and so on. After running out of
placeholders, final tab will land at `$0` which is useful for leaving the
snippet without having to manually placing the cursor.

As another example, I have created two snippets for my
[Hugo shortcodes](https://github.com/parsiya/Hugo-Shortcodes):

``` json
{
    "codecaption": {
		"prefix": "codecap",
		"body": [
            // comment is a placeholder to prevent Hugo from generating the shortcode.
			"{{</* codecaption title=\"${1:title}\" lang=\"${2:language}\" */>}}",
			"${3:code}",
			"{{</* /codecaption */>}}",
			"", // empty line after shortcode
			"$0"
		],
		"description": "codecaption Hugo shortcode"
	},
	"imgcap": {
		"prefix": "imgcap",
		"body": [
			"{{< imgcap title=\"${1:title}\" src=\"${2:filename}.png\" >}}",
			"$0"
		],
		"description": "image caption Hugo shortcode"
	},
}
```
