# Random Code
This repository contains most of the code that I write for my blog posts. I realized I have random repositories on Github and am consolidating them into one.

## Individual Licenses
Most code in this repository is governed under the [MIT](../LICENSE-code). Some code may have a different license, check each directory for a license file.

## Code Index
This table will help.

<!-- MarkdownTOC -->

- [WinAppDbg Tutorials](#winappdbg-tutorials)
- [Cryptopals - Golang](#cryptopals---golang)
- [Hipchat Proxy](#hipchat-proxy)
- [.NET Remoting](#net-remoting)
- [Malware Adventure](#malware-adventure)
- [Octopress Image Popup Plugin Forked](#octopress-image-popup-plugin-forked)

<!-- /MarkdownTOC -->

<a name="winappdbg-tutorials"></a>
### [WinAppDbg Tutorials](winappdbg)
Code for my set of WinAppDbg tutorials.

1. Copy the `winappdbg` directory to your Virtual Machine.
2. Install Python, WinAppDbg and other software using instructions in part 1.
3. Follow the tutorials and enjoy.
4. If code is wrong, make an issue here or yell at me on Twitter/email/etc.

- [Part 1 - Basics][winappdbg-1]
- [Part 2 - Function Hooking and Others][winappdbg-2]
- [Part 3 - Manipulating Function Calls][winappdbg-3]
- [Part 4 - Bruteforcing FlareOn 2017 - Challenge 3][winappdbg-4]

<a name="cryptopals---golang"></a>
### [Cryptopals - Golang](cryptopals/go)
Doing the Cryptopals challenges with `lol no generics`.

<a name="hipchat-proxy"></a>
### [Hipchat Proxy](hipchat-proxy)
Small proxy that I wrote for proxying Hipchat.

- Main blog post
    - [Proxying Hipchat Part 3: SSL Added and Removed Here][hipchat-3]
- Related blogs:
    - [Proxying Hipchat Part 1: Where did the Traffic Go?][hipchat-1]
    - [Proxying Hipchat Part 2: So You Think You Can Use Burp?][hipchat-2]

<a name="net-remoting"></a>
### [.NET Remoting](net-remoting)
Code and example program used in:

- [Intro to .NET Remoting for Hackers][net-remoting]

<a name="malware-adventure"></a>
### [Malware Adventure](malware-adventure)
Small text adventure written in Python using PAWS (Python Adventure Writing System). Created as part of the class activity for "Advanced Topics in Computer Security" in 2013 at Johns Hopkins.

PAWS 2.1 is a fork by `Matthias C. Hormann` at [https://github.com/Moonbase59/PAWS][paws-github]. PAWS was originally created by `Roger Plowman`.

- Blog post
    - [Malware Adventure][malware-adventure-blog]
- Github repository (because there are links to it)
    - [https://github.com/parsiya/malwareadventure][malware-adventure-github]

<a name="octopress-image-popup-plugin-forked"></a>
### [Octopress Image Popup Plugin Forked](https://github.com/parsiya/octopress-image-popup-forked)
This is a fork of the the Octopress Image Popup Plugin at [https://github.com/ctdk/octopress-image-popup][original-popup] by Jeremy Bingham. The original instructions did not work for me out of the box so I made some minor changes. Because it has a different license, I am keeping it in a separate repository.

- Blog post
    - [Image Popup and Octopress][pop-up-blog].


<!-- Links -->

[hipchat-1]: https://parsiya.net/blog/2015-10-08-proxying-hipchat-part-1-where-did-the-traffic-go/
[hipchat-2]: https://parsiya.net/blog/2015-10-09-proxying-hipchat-part-2-so-you-think-you-can-use-burp/
[hipchat-3]: https://parsiya.net/blog/2015-10-19-proxying-hipchat-part-3-ssl-added-and-removed-here/
[net-remoting]: https://parsiya.net/blog/2015-11-14-intro-to-.net-remoting-for-hackers/
[original-popup]: https://github.com/ctdk/octopress-image-popup
[pop-up-blog]: https://parsiya.net/blog/2015-07-26-image-popup-and-octopress/
[pop-up-github]: https://github.com/parsiya/octopress-image-popup-forked
[paws-github]: https://github.com/Moonbase59/PAWS
[malware-adventure-blog]: https://parsiya.net/blog/2014-09-21-malware-adventure/
[malware-adventure-github]: https://github.com/parsiya/malwareadventure
[winappdbg-1]: https://parsiya.net/blog/2017-11-09-winappdbg---part-1---basics/
[winappdbg-2]: https://parsiya.net/blog/2017-11-11-winappdbg---part-2---function-hooking-and-others/
[winappdbg-3]: https://parsiya.net/blog/2017-11-15-winappdbg---part-3---manipulating-function-calls/
[winappdbg-4]: https://parsiya.net/blog/2017-11-15-winappdbg---part-4---bruteforcing-flareon-2017---challenge-3/
