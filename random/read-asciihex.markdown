---
draft: false
toc: false
comments: false
categories:
- Random
tags:
- ascii-hex
title: "Printable ASCII-Hex"
wip: false
snippet: "Reading ASCII-Hex, the lazy way!"
---

Reading ASCII-Hex is easy. When you see a bunch of hex bytes, you can usually
figure out if it's text or not by dropping them into a decoder. However, there
are things you can memorize to save you a few seconds. What I have learned:

* Printable ASCII-Hex characters start from `0x20` (space) and end at `0x7F`.
* `0x3N` is a number with `N` being the number. For example, `0x30` is `0` and `0x39` is `9`.
* Capital letters start from `0x41` (`A`) to `0x61` (`Z`).
* Add `0x20` to a capital letter to get the small one. E.g. `0x41 (A) + 0x20 = 0x61 (a)`. 

An ASCII table that I have to Google all the time:

{{< imgcap title="ASCII-Hex from https://www.asciitable.com/index/asciifull.gif" src="https://www.asciitable.com/index/asciifull.gif" >}}
