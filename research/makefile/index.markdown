---
title: "Makefile Notes"
date: 2022-11-30T15:47:17-08:00
draft: false
toc: true
comments: false
categories:
- Random
tags:
- Makefile
wip: false
snippet: "Notes about creating a Makefile."
---

Most of this is about [GNU Make][gnumake] but should work with others.

[gnumake]: https://www.gnu.org/software/make/

> If you want to find someone who likes to use both tabs and spaces as different
> separators in a text file, talk to the guy who invented Makefiles!
>
> - Me

A makefile has a bunch of rules. Each rule has a target, some prerequisites
(e.g., files) and a recipe. A recipe is a series of commands.

```makefile
target: prereqs
[tab]   command1
        command2
        command3
```

The recipe should start with a `tab`. But you also need to indent some other
things (e.g., conditionals) with space. This will be a mess.

## Use RECIPEPREFIX
To make your life easier, add this to the beginning of your makefile to replace
tab with another character.

```makefile
.RECIPEPREFIX := > # use `>` instead of `\t`
```

Now, your file looks like this:

```makefile
target: prereqs
> command1
> command2
> command3
```

## PHONY
You can run each target with `make target`. However, if `target` also exists as
a file in the target directory, it will interfere. See [Phony Targets][phony].

```makefile
.PHONY: target
target: prereqs
> command1
> command2
> command3
```

[phony]: https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html

## Conditionals
Conditionals are different from programming languages. They do not necessarily
control the program flow but they hide/unhide instructions. Think of them as
`IFDEF`s in C. Let's use an example.

## Detect if Command Exists
I have tested this on Linux. It's supposedly POSIX compliant but I don't know if
it works on other OS yet. For example, if we want to check Python3 exists.

```makefile
target:
# check if python3 exists
ifeq ($(shell command -v python3 2> /dev/null), )
> $(error python3 not installed)
endif
```

`error` will terminate the makefile with an error.

Let's say you want to check if Semgrep exists and if not, install it.

```makefile
target:
# install Semgrep if it's not installed
ifeq ($(shell command -v semgrep 2> /dev/null), )
> python3 -m pip install semgrep
> $(info you might have to add ~/.local/bin to PATH)
endif
```

`info` prints some information.

## Parallel Tasks
You can parallelize the commands in the recipe instead of sequentially running
them. This can be done with `-j` (infinite) or `-j number-of-parallel-jobs`.

This is useful when each command is different. For example, building Go binaries
for different platforms. Note the use of the variable `BINARY_NAME`.

```makefile
BINARY_NAME := myapp

.PHONY: build-all
build-all:
> GOARCH=arm64 GOOS=darwin go build -o ${BINARY_NAME}-darwin-arm64 -ldflags "-w -s" main.go
> GOARCH=amd64 GOOS=darwin go build -o ${BINARY_NAME}-darwin-amd64 -ldflags "-w -s" main.go
> GOARCH=arm64 GOOS=linux  go build -o ${BINARY_NAME}-linux-arm64  -ldflags "-w -s" main.go
> GOARCH=amd64 GOOS=linux  go build -o ${BINARY_NAME}-linux-amd64  -ldflags "-w -s" main.go
```

## Run Multiple Targets
You can have targets that run other ones. A popular target is `all`.

```makefile
.PHONY: all
all: clean build deploy
```

This is an alternate way of writing a recipe. This is the same as below:

```makefile
.PHONY: all
all:
> clean
> build
> deploy
```

Now we can run `make all` to run all these targets.

## The Help Target
If no argument is provided, make will run the first target. It's a good idea for
the first target to be the help/usage. We can print something manually:

```makefile
.PHONY: help
help:
> $(info Usage)
> $(info make help     print help)
> $(info make all      clean, test and build)
> $(info make install  install dependencies)
```

We can also do it automatically. I forgot where I copied the code from but there
are multiple versions all over the internet.

```makefile
.PHONY: help
help:   ## print help
> @sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

.PHONY: all
all:    ## clean, deploy, and build
> clean
> build
> deploy
```

If we run `make help` or `make` (help is the first target) we will see:

```
help:   ## print help
all:    ## clean, deploy, and build
```

This is an issue if we have prerequisites. One of the other similar commands
might fix this but I did not investigate. Note, we have to manually fix the
whitespace between the target and the comment.