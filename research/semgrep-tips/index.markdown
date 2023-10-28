---
draft: false
toc: true
comments: false
categories:
- Research
title: "Semgrep Tips and Tricks"
wip: true
snippet: "[Semgrep](https://semgrep.dev/) stuff that I always forget."
---

# Semgrep on Windows via WSL
As of today (November 2022), **you cannot run Semgrep directly on Windows**.
Seriously, save your sanity and don't try. But you can run it in the
[Windows Subsystem for Linux][wsl].

[wsl]: https://learn.microsoft.com/en-us/windows/wsl/

## Install WSL
I won't go into the details. Use the
[Install Linux on Windows with WSL][wsl-install] guide from Microsoft.

[wsl-install]: https://learn.microsoft.com/en-us/windows/wsl/install

## Which Distro Should I Choose?
It's your call. My current daily WSL2 driver is Debian 11. I have used Semgrep
in multiple versions of Ubuntu and Debian without issues.

Make sure you're using a recent distro that supports installing Python 3.7 or
higher via its package manager (why install it manually when you can make your
life easier?).

Note you can [have multiple versions of the same distro][wsl-import-export].

[wsl-import-export]: https://parsiya.net/cheatsheet/#import-and-export

## WSL1 vs. WSL2
See [Comparing WSL 1 and WSL 2][wsl-compare].

[wsl-compare]: https://learn.microsoft.com/en-us/windows/wsl/compare-versions

**Are most of your files on the Windows file system? Use WSL1.**

WSL2 uses Hyper-V and so has good performance for files on its own file system
(e.g., `~/...`). I use WSL2.

**Are you behind a corporate proxy or use VPN software (e.g., Cisco AnyConnect)?
Use WSL1.**

WSL2 uses Hyper-V. Hyper-V has issues connecting to VPN when you use certain VPN
software. I have spent hundreds of hours trying to fix it. You might think you
can do too but just use WSL1 and save some of your time.

[WSL2 also does not get inotify events for files on the Windows file system][wsl2-inotify].

[wsl2-inotify]: https://parsiya.io/random/wsl2-hugo-watch/

**Easily switch between WSL1 and WSL2**

`wsl -l -v` to see all the distros.

`wsl --set-version <distro name> 2` or `wsl --set-version <distro name> 1`.

It might take a few minutes to copy the files but it generally works.

## Install Semgrep on WSL
`python3 -m pip install semgrep` or `python -m pip install semgrep` (depending
on distro).

### Semgrep Command not Found

1. Look for Semgrep in `~/.local/bin`.
2. Add it to your path by adding the following line to `~/.bashrc` or
   `~/.profile` (my preference).
   * `export PATH=$PATH:~/.local/bin`
3. Run `source ~/.profile` or `source ~/.bashrc` to make the change.

# Configs

## Download a Ruleset YAML File
This will download the YAML file with all the rules.

```
# p/{ruleset-name}

# this will download the default ruleset in a file named `default`
wget https://semgrep.dev/c/p/default

# note it's capital O (O as in Oscar, not zero)
wget https://semgrep.dev/c/p/default -O default.yaml

# you can also use curl or even your browser
curl https://semgrep.dev/c/p/default
```

**Note:** These URLs are for internal usage and are subject to change.

## Run ALL the Rules

* Throw the kitchen sink at your code: `--config r/all`.
* Run the manually created "catch them all" scan: `--config p/default`.

Note: Semgrep is intelligent and detects a file's language by extension so it
will not every rule on every file.

# Sample Rules
Some fun things to do with Semgrep.

## Double Matches with Different Semgrep Messages
I was printing the type of a metavariable.
https://semgrep.dev/playground/s/parsiya:tips-double-match

```yaml
rules:
  - id: tips-double-match
    pattern: $RETTYPE $METHOD() { ... }
    message: $RETTYPE
    severity: WARNING
    languages:
      - java
```

It was matched twice.

```java
package pk;

import org.foo.bar.MyType;

public class MyClass {

    public MyType method() {
        // do something
        return MyType("123");
    }
}
```

Once with the type and once with the complete import name.

```
Line 7
MyType

Line 7
org.foo.bar.MyType
```

### Fix
One fix (credit: [Lewis Ardern, Semgrep][lewis-gh],
[source][lewis-double-match-answer]) is to add it to `focus-metavariable`. Note,
how we need to add `patterns` to have `focus-metavariable` as a tag.

https://semgrep.dev/playground/s/parsiya:tips-double-match-fix

```yaml
rules:
  - id: tips-double-match-fix
    patterns:
      - pattern: $RETTYPE $METHOD() { ... }
      - focus-metavariable: $RETTYPE
    message: $RETTYPE
    severity: WARNING
    languages:
      - java
```

[lewis-double-match-answer]: https://r2c-community.slack.com/archives/C018NJRRCJ0/p1666654970257119?thread_ts=1666654882.737839&cid=C018NJRRCJ0
[lewis-gh]: https://github.com/LewisArdern

### Explanation
Credit: [Iago Abal][iago-gh], Semgrep, [source on Semgrep slack][iago-double-match-answer].

[iago-gh]: https://github.com/IagoAbal
[iago-double-match-answer]: https://r2c-community.slack.com/archives/C018NJRRCJ0/p1666705798027529?thread_ts=1666654882.737839&cid=C018NJRRCJ0

> For Semgrep `MyType` is also equivalent to `org.foo.bar.MyType`, so when you
ask Semgrep to match `$RETTYPE` against `MyType` it produces those two matches.
And because `$RETTYPE` is part of the rule message, each match produces a
different message, and **Semgrep doesn't deduplicate two findings if each
finding has a different message**. I think `focus-metavariable` removes the
duplicate because the "fake" `org.foo.bar.MyType` expression that we generate as
equivalent to `MyType` uses tokens from the `import` and so the ranges of those
tokens do not intersect with the method declaration... I see that more like a
bug.

> These double-matches you can observe them with other equivalences as in
https://semgrep.dev/s/QDdD, because `&` is commutative and Semgrep does some
AC-matching, `$A` may be both `x` and `y`, so you get two matches.

## Skipping Java Annotations
Assume we have a file like this:

```java
@Annotation1
public class ParentClass {

    @First
    @Second
    @Third
    public int meth1() {
        return 1;
    }
}
```

And I wanted to skip all annotations after `@First`. This is not a valid pattern:

```yaml
pattern: |
  @First
  ...
  public $RETURNTYPE $METHOD(...) { ... }
```

https://semgrep.dev/playground/s/parsiya:tips-java-annotations

### Fix
Credit: [Cooper Pierce][cooper-gh], Semgrep, [source on Semgrep slack][annotation-answer].

> annotations beyond those specified are ignored when matching so something like
> [the following] would do what you describe

[cooper-gh]: https://github.com/kopecs
[annotation-answer]: https://r2c-community.slack.com/archives/C018NJRRCJ0/p1666327030925379?thread_ts=1666326171.514289&cid=C018NJRRCJ0

```yaml
rules:
  - id: tips-java-annotations
    pattern: |
      @First
      public $RETURNTYPE $METHOD(...) { ... }
    message: |
      $CLASS
    severity: WARNING
    languages:
      - java
```

https://semgrep.dev/playground/s/parsiya:tips-java-annotations-fix

## pattern-inside AND & OR
This is `AND`. The match must satisfy both.

```yaml
- pattern-inside: ...
- pattern-inside: ...
```

This is `OR`.

```yaml
- pattern-either:
  - pattern-inside: ...
  - pattern-inside: ...
```

## if Statements in C/C++
Capture Conditions of `if` Statements in C/C++: `if ($X)`.

Capture `if` conditions with one line blocks.

https://semgrep.dev/playground/s/parsiya:tips-detect-single-line-if-block

```yaml
rules:
  - id: detect_if
    patterns:
      - pattern: if ($X) ...
      - pattern-not: if ($X) { $Y; ... }
    message: Found a one-line if block
    languages:
      - c
    severity: WARNING
```

Credit: [Cooper Pierce][cooper-gh], Semgrep, [source on Semgrep slack][single-block-if].

[single-block-if]: https://r2c-community.slack.com/archives/C018NJRRCJ0/p1660943282982279?thread_ts=1660942419.479839&cid=C018NJRRCJ0

## Array Arguments in C/C++
`$TYPE $VAR[...];` is not valid, use `$TYPE $VAR[$SIZE];`. This also matches
multi-dimensional arrays like `int nDim_init[10][10][10][10][10][10];`.

**In general:** Use metavariables instead of `...` in C/C++.

### Explanation

> `...` is usually reserved to match a sequence of things (e.g., `foo(...)`), or
> if something is optional (e.g., `return ...;`)

Credit: [Padioleau Yoann][yoann-gh], Semgrep, [source: Semgrep slack][c-ellipsis].

[yoann-gh]: https://github.com/aryx
[c-ellipsis]: https://r2c-community.slack.com/archives/C018NJRRCJ0/p1648051884724009?thread_ts=1648001009.133229&cid=C018NJRRCJ0

## Alert if a Specific File or Path Exists
Unconventional but we can write a rule like this:

```yaml
rules:
- id: detect-file
  patterns:
    - pattern-regex: .*
  message: Semgrep found the file
  languages:
    - generic
  severity: WARNING
  paths:
    include:
      - /path/to/badfile*
    exclude:
      - /paths/to/exclude/*
```

https://semgrep.dev/playground/s/parsiya:detect-file

The path is relative to where you run Semgrep. The file doesn't need to have
any content. [paths > include/exclude][paths] should give us a lot of power to
detect different paths.

[paths]: https://semgrep.dev/docs/writing-rules/rule-syntax/#paths

Credit: Yours Truly, Parsia, [source: Semgrep slack][file-detect].

[file-detect]: https://r2c-community.slack.com/archives/C018NJRRCJ0/p1670547075635089?thread_ts=1670540633.760339&cid=C018NJRRCJ0

## Alert if JavaScript Imports Exist and are Used
This was asked in the Semgrep slack and I came up with this answer that I liked.
We want to get a match if there are a few specific JavaScript imports in a file
and if they are _all_ used. The order of imports and usage shouldn't matter.
Here's an example:

```js
var os = require("os");
var http = require("http");
var dns = require("dns");
os.exec("ls");
http.get("something");
dns.something("whatever");
let a = 1;
```

The rule takes advantage of having creating a union of six different
`pattern-inside` clauses (three for imports and three for usages). It will match
everything after all six patterns are met.

Semgrep playground link:
https://semgrep.dev/playground/s/parsiya:three-imports-used.

```yaml
rules:
- id: three-imports-used
  patterns:
    - pattern-inside: |
        $OS = require('os')
        ...
    - pattern-inside: |
        $HTTP = require('http')
        ...
    - pattern-inside: |
        $DNS = require('dns')
        ...
    - pattern-inside: |
        $OS.$METHOD1(...)
        ...
    - pattern-inside: |
        $HTTP.$METHOD2(...)
        ...
    - pattern-inside: |
        $DNS.$METHOD3(...)
        ...
  message: Semgrep found a match
  languages:
    - js
  severity: WARNING
```

## Using pattern-metavariable with Language Generic
This is a neat trick from my good friend [Lewis Ardern][lewis-gh]. The question
on the Semgrep Slack wanted to match text in a bash file like this:
`openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:1024`.
The extracted info was supposed to be the `1024` number. Then the rule had to
check if the number was less than `2048`.

I faced a problem here. It's not possible to create a Semgrep pattern like this
for bash.

```yaml
pattern: openssl ... -pkeyopt rsa_keygen_bits:$BITS ...
```

I guess it's because of the way tree-sitter creates tokens in bash. But I could
create a pattern like this and get `rsa_keygen_bits:1024` completely:

```yaml
pattern: openssl ... -pkeyopt $RSA ...
```

We can use a `pattern-metavariable` with the `generic` language to do text
processing here which allows us to extract the number in a metavariable and also
use `metavariable-comparison`.

```yaml
patterns:
  - pattern: |
      openssl ... -pkeyopt $KEY ...
  - metavariable-pattern:
      metavariable: $KEY
      language: generic
      patterns:
        - pattern: rsa_keygen_bits:$BITS ...
        - metavariable-comparison:
            comparison: $BITS < 2048
  - focus-metavariable:
      - $BITS
```

Complete rule: https://semgrep.dev/playground/s/6YQ1


# Rule Tests

## Test File Names for Rules with the paths Tag
I had a rule that was looking for `*-NAME.cpp` files. E.g.,

```yaml
rules:
- id: some-rule
  languages:
    - cpp
  paths:
    include:
      - "*-NAME.cpp"
```

The test file should match one of the items in `include`. In this case, I needed
to rename the test file `some-rule-NAME.cpp`.

# Memes

## You Made This?
Edits to the famous comic: Yours Truly, Parsia.

![You Made This?](you-made-this.png)
