# Parsiya Clone
This my clone. I have been maintaining one internally at Cigital/Synopsys since mid 2016. It has been decently successful and well received. I have decided to make a public one too. There is going to be a lot of redundancy between here and my [website][parsiya.net] but that is expected. This repository will also contain code and random notes that do not get published there effectively removing the Random-Code and Random-Notes repositories I recently started.

## Table of Contents
<!-- MarkdownTOC -->

- [Clone](#clone)
    - [Cheat Sheet](#cheat-sheet)
    - [Abandoned "Research"](#abandoned-research)
        - [BMC Track It 11.2](#bmc-track-it-112)
    - [Random](#random)
        - [Migration from Octopress to Hugo](#migration-from-octopress-to-hugo)
- [Code](#code)
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
### [Cheat Sheet](cheatsheet.md)
Copy of [https://parsiya.net/cheatsheet/][cheat-sheet-ext].

<a name="abandoned-research"></a>
### [Abandoned "Research"](clone/abandoned-research)
I started something but gave up in the middle. You can find my notes here.

<a name="bmc-track-it-112"></a>
#### [BMC Track It 11.2](clone/abandoned-research/BMC-Track-It-11.2.md)
Attempting to reproduce a .NET Remoting vulnerability.

<a name="random"></a>
### [Random](clone/random)
Random stuff that do not belong anywhere else.

<a name="migration-from-octopress-to-hugo"></a>
#### [Migration from Octopress to Hugo](clone/random/octopress-migration.md)
Random scripts used to convert my Octopress blog to [Hugo][hugo-link], [blog posts][hugo-posts].

<!-- End Clone -->

<!-- Start Code -->
<a name="code"></a>
## Code

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

<!-- End Links -->