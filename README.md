# Parsiya Clone
This is my clone. I have been maintaining one internally at Cigital/Synopsys since mid 2016. It has been decently successful and well received. I have decided to make a public one too. There is going to be a lot of redundancy between here and my [website][parsiya.net] but that is expected. This repository will also contain code and random notes that do not get published there effectively removing the Random-Code and Random-Notes repositories I recently started.

## Table of Contents
<!-- MarkdownTOC -->

- [Clone](#clone)
    - [Cheat Sheet](#cheat-sheet)
    - ["Research" Notes](#research-notes)
        - [Razer Comms](#razer-comms)
    - [Random](#random)
        - [Migration from Octopress to Hugo](#migration-from-octopress-to-hugo)
        - [Call Windows APIs in C/C++ using MinGW](#call-windows-apis-in-cc-using-mingw)
        - [Windows SearchPath](#windows-searchpath)
    - [Abandoned "Research"](#abandoned-research)
        - [BMC Track It 11.2](#bmc-track-it-112)
- [Code](#code)
    - [WinAppDbg Tutorials](#winappdbg-tutorials)
    - [Hipchat Proxy](#hipchat-proxy)
    - [Intro to .NET Remoting for Hackers](#intro-to-net-remoting-for-hackers)
    - [Malware Adventure](#malware-adventure)
    - [Octopress Image Popup Plugin Forked](#octopress-image-popup-plugin-forked)
- [License](#license)
- [TODO](#todo)

<!-- /MarkdownTOC -->

<!-- Start Clone -->
<a name="clone"></a>
## Clone

<a name="cheat-sheet"></a>
### [Cheat Sheet](cheat-sheet.md)
Copy of [https://parsiya.net/cheatsheet/][cheat-sheet-ext].

-----

<a name="research-notes"></a>
### ["Research" Notes](clone/research)
Stuff I have done, most of these have their own blog posts. The extra notes are here.

<a name="razer-comms"></a>
#### [Razer Comms](clone/research/razer-comms/)
Razer Comms [mini report][razer-comms-blog] and notes.

-----

<a name="random"></a>
### [Random](clone/random)
Random stuff that do not belong anywhere else.

<a name="migration-from-octopress-to-hugo"></a>
#### [Migration from Octopress to Hugo](clone/random/octopress-migration.md)
Random scripts used to convert my Octopress blog to [Hugo][hugo-link], [blog posts][hugo-posts].

<a name="call-windows-apis-in-cc-using-mingw"></a>
#### [Call Windows APIs in C/C++ using MinGW](clone/random/mingw-windows.md)
Notes on installing gcc on Windows and calling Windows APIs in C/C++.

<a name="windows-searchpath"></a>
#### [Windows SearchPath](clone/random/search-path.md)
Notes about Windows SearchPath.

-----

<a name="abandoned-research"></a>
### [Abandoned "Research"](clone/abandoned-research)
I started these things but gave up in the middle. You can find my notes here.

<a name="bmc-track-it-112"></a>
#### [BMC Track It 11.2](clone/abandoned-research/BMC-Track-It-11.2.md)
Attempting to reproduce a .NET Remoting vulnerability.

<!-- End Clone -->

-----

<!-- Start Code -->
<a name="code"></a>
## Code

<a name="winappdbg-tutorials"></a>
### [WinAppDbg Tutorials](code/winappdbg)
Code for my set of WinAppDbg tutorials.

1. Copy the `winappdbg` directory to your Virtual Machine.
2. Install Python, WinAppDbg and other software using instructions in part 1.
3. Follow the tutorials and enjoy.
4. If code is wrong, make an issue here or yell at me on Twitter/blog/etc.

- [Part 1 - Basics][winappdbg-1]
- [Part 2 - Function Hooking and Others][winappdbg-2]
- [Part 3 - Manipulating Function Calls][winappdbg-3]

<a name="hipchat-proxy"></a>
### [Hipchat Proxy](code/hipchat-proxy)
Small proxy written in Python for Hipchat, [blog posts][hipchat-posts].

<a name="intro-to-net-remoting-for-hackers"></a>
### [Intro to .NET Remoting for Hackers](code/net-remoting)
Sample C# application to demonstrate a .NET remoting vuln, [blog][net-remoting].

<a name="malware-adventure"></a>
### [Malware Adventure](code/malware-adventure)
Small text adventure written in Python using PAWS (Python Adventure Writing System).

<a name="octopress-image-popup-plugin-forked"></a>
### [Octopress Image Popup Plugin Forked](https://github.com/parsiya/octopress-image-popup-forked)
Fork of the the [Octopress Image Popup Plugin][original-popup] by Jeremy Bingham.

<!-- End Code -->

<a name="license"></a>
## License
These licenses only apply to **my code and non-code content** in this clone. In short I want people to be able to use anything if they want to with attribution and without warranty.

- Code is open sourced under the [MIT license](LICENSE-code).
- Non-code content is licensed under [Creative Commons Attribution-NonCommercial 4.0][CC-license] (CC BY-NC 4.0).

This repository will inevitably contain content from other parts of the internet. I will do my best to comply with licenses and provide attribution. If you see any issues please contact me.

<a name="todo"></a>
## TODO
1. Add FAQ.
2. ~~Add cheat sheet from website.~~
    - Find a way to keep the cheat sheet here updated when I modify the other one. 


<!-- Start Links -->

[parsiya.net]: https://parsiya.net
[CC-license]:  https://creativecommons.org/licenses/by-nc-sa/4.0/
[hipchat-posts]: https://parsiya.net/categories/hipchat/
[net-remoting]: https://parsiya.net/blog/2015-11-14-intro-to-.net-remoting-for-hackers/
[original-popup]: https://github.com/ctdk/octopress-image-popup
[cheat-sheet-ext]: https://parsiya.net/cheatsheet
[hugo-posts]: https://parsiya.net/categories/migration-to-hugo/
[hugo-link]: https://gohugo.io/
[razer-comms-blog]: https://parsiya.net/blog/2017-09-21-razer-comms/
[winappdbg-1]: https://parsiya.net/blog/2017-11-09-winappdbg---part-1---basics/
[winappdbg-2]: https://parsiya.net/blog/2017-11-11-winappdbg---part-2---function-hooking-and-others/
[winappdbg-3]: https://parsiya.net/blog/2017-11-15-winappdbg---part-3---manipulating-function-calls/

<!-- End Links -->