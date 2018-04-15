# Parsia Clone
This is my clone. I have been maintaining one internally at Cigital/Synopsys since mid 2016. It has been decently successful and well received. I have decided to make a public one too. There is going to be a lot of redundancy between here and my [website][parsiya.net] but that is expected. This repository will also contain code and random notes that do not get published there effectively removing the Random-Code and Random-Notes repositories I recently started.

## Table of Contents
<!-- MarkdownTOC autolink=true autoanchor=true -->

- [Clone](#clone)
    - [Presentations](#presentations)
        - [Blockchain Security at NoVA Hackers - PDF](#blockchain-security-at-nova-hackers---pdf)
    - ["Research" Notes](#research-notes)
        - [Razer Comms](#razer-comms)
    - [Configurations](#configurations)
        - [Sublime Text 3 Config and Packages](#sublime-text-3-config-and-packages)
        - [Ubuntu 16 Setup](#ubuntu-16-setup)
    - [Random](#random)
        - [FlareOn 2017 CTF Notes](#flareon-2017-ctf-notes)
        - [Migration from Octopress to Hugo](#migration-from-octopress-to-hugo)
        - [Call Windows APIs in C/C++ using MinGW](#call-windows-apis-in-cc-using-mingw)
        - [Windows SearchPath](#windows-searchpath)
        - [Converting Pygments Styles to Chroma](#converting-pygments-styles-to-chroma)
    - [Abandoned "Research"](#abandoned-research)
        - [BMC Track It 11.2](#bmc-track-it-112)
        - [Learning Triton](#learning-triton)
- [Code](#code)
    - [WinAppDbg Tutorials](#winappdbg-tutorials)
    - [Cryptopals - Golang](#cryptopals---golang)
    - [Go - Infosec](#go---infosec)
        - [SSH Harvester](#ssh-harvester)
        - [pcap Tutorial](#pcap-tutorial)
    - [Hipchat Proxy](#hipchat-proxy)
    - [Intro to .NET Remoting for Hackers](#intro-to-net-remoting-for-hackers)
    - [Malware Adventure](#malware-adventure)
    - [Octopress Image Popup Plugin Forked](#octopress-image-popup-plugin-forked)
- [License](#license)
- [TODO](#todo)

<!-- /MarkdownTOC -->

<!-- Start Clone -->
<a id="clone"></a>
## Clone

<a id="presentations"></a>
### Presentations
Random slides.

<a id="blockchain-security-at-nova-hackers---pdf"></a>
#### [Blockchain Security at NoVA Hackers - PDF](clone/presentations/BlockchainSecurityin30Minutes-Parsia-NoVAHackers-March12-2018.pdf)
Also on [Google Drive][blockchain-security-1].

<a id="research-notes"></a>
### ["Research" Notes](clone/research)
Stuff I have done, most of these have their own blog posts. The extra notes are here.

<a id="razer-comms"></a>
#### [Razer Comms](clone/research/razer-comms/)
Razer Comms [mini report][razer-comms-blog] and notes.

-----

<a id="configurations"></a>
### [Configurations](clone/configs)
Configurations for Operating Systems, editors and other programs.

<a id="sublime-text-3-config-and-packages"></a>
#### [Sublime Text 3 Config and Packages](clone/configs/sublime-text)
My Sublime Text 3 config files and packages, [blog post][from-atom-to-sublime].

<a id="ubuntu-16-setup"></a>
#### [Ubuntu 16 Setup](clone/configs/ubuntu-16-setup.md)
Setup instructions for configuring a new Ubuntu VM.

-----

<a id="random"></a>
### [Random](clone/random)
Random stuff that do not belong anywhere else.

<a id="flareon-2017-ctf-notes"></a>
#### [FlareOn 2017 CTF Notes](clone/random/flareon-2017)
Random notes from FlareOn 2017 Reverse Engineering CTF.

<a id="migration-from-octopress-to-hugo"></a>
#### [Migration from Octopress to Hugo](clone/random/octopress-migration.md)
Random scripts used to convert my Octopress blog to [Hugo][hugo-link], [blog posts][hugo-posts].

<a id="call-windows-apis-in-cc-using-mingw"></a>
#### [Call Windows APIs in C/C++ using MinGW](clone/random/mingw-windows.md)
Notes on installing gcc on Windows and calling Windows APIs in C/C++.

<a id="windows-searchpath"></a>
#### [Windows SearchPath](clone/random/search-path.md)
Notes about Windows SearchPath.

<a id="converting-pygments-styles-to-chroma"></a>
#### [Converting Pygments Styles to Chroma](clone/random/chroma-pygments-convert)
Instructions for converting a Pygments style to [Chroma][chroma].

-----

<a id="abandoned-research"></a>
### [Abandoned "Research"](clone/abandoned-research)
I started these things but gave up in the middle. You can find my notes here.

<a id="bmc-track-it-112"></a>
#### [BMC Track It 11.2](clone/abandoned-research/BMC-Track-It-11.2.md)
Attempting to reproduce a .NET Remoting vulnerability.

<a id="learning-triton"></a>
#### [Learning Triton](clone/abandoned-research/learning-triton.md)
Notes on [Triton](https://triton.quarkslab.com/) installation.

<!-- End Clone -->

-----

<!-- Start Code -->
<a id="code"></a>
## Code

<a id="winappdbg-tutorials"></a>
### [WinAppDbg Tutorials](code/winappdbg)
Code for my set of WinAppDbg tutorials.

1. Copy the `winappdbg` directory to your Virtual Machine.
2. Install Python, WinAppDbg and other software using instructions in part 1.
3. Follow the tutorials and enjoy.
4. If code is wrong, make an issue here or yell at me on Twitter/blog/etc.

- [Part 1 - Basics][winappdbg-1]
- [Part 2 - Function Hooking and Others][winappdbg-2]
- [Part 3 - Manipulating Function Calls][winappdbg-3]
- [Part 4 - Bruteforcing FlareOn 2017 - Challenge 3][winappdbg-4]

<a id="cryptopals---golang"></a>
### [Cryptopals - Golang](code/cryptopals/go)
Doing the Cryptopals challenges with Go.

<a id="go---infosec"></a>
### [Go - Infosec](code/go-infosec/)
New Go security projects will be in a different repository at:

- [https://github.com/parsiya/Go-Security](https://github.com/parsiya/Go-Security)

<a id="ssh-harvester"></a>
#### [SSH Harvester](go-infosec/ssh-harvester)
Initial version of tool written in Go that harvests SSH certificates. For explanation of code please see the blog post [Simple SSH Harvester in Go][go-sshharvester].

<a id="pcap-tutorial"></a>
#### [pcap Tutorial](code/go-infosec/pcap-tutorial)
Code for the blog post [Go and pcaps][go-pcap] which explains how to use Go to extract icmp echo payloads from a pcap file.

<a id="hipchat-proxy"></a>
### [Hipchat Proxy](code/hipchat-proxy)
Small proxy written in Python for Hipchat, [blog posts][hipchat-posts].

<a id="intro-to-net-remoting-for-hackers"></a>
### [Intro to .NET Remoting for Hackers](code/net-remoting)
Sample C# application to demonstrate a .NET remoting vuln, [blog][net-remoting].

<a id="malware-adventure"></a>
### [Malware Adventure](code/malware-adventure)
Small text adventure written in Python using PAWS (Python Adventure Writing System).

<a id="octopress-image-popup-plugin-forked"></a>
### [Octopress Image Popup Plugin Forked](https://github.com/parsiya/octopress-image-popup-forked)
Fork of the the [Octopress Image Popup Plugin][original-popup] by Jeremy Bingham.

<!-- End Code -->

<a id="license"></a>
## License
These licenses only apply to **my code and non-code content** in this clone. In short I want people to be able to use anything if they want to with attribution and without warranty.

- Code is open sourced under the [MIT license](LICENSE-code).
- Non-code content is licensed under [Creative Commons Attribution-NonCommercial 4.0][CC-license] (CC BY-NC 4.0).

This repository will inevitably contain content from other parts of the internet. I will do my best to comply with licenses and provide attribution. If you see any issues please contact me.

<a id="todo"></a>
## TODO
1. Add FAQ.
2. ~~Add cheat sheet from website.~~ Removed cheat sheet, no need to have two copies.
    - ~~Find a way to keep the cheat sheet here updated when I modify the other one.~~


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
[winappdbg-4]: https://parsiya.net/blog/2017-11-15-winappdbg---part-4---bruteforcing-flareon-2017---challenge-3/
[go-pcap]: https://parsiya.net/blog/2017-12-03-go-and-pcaps/
[go-sshharvester]: https://parsiya.net/blog/2017-12-28-simple-ssh-harvester-in-go/
[blockchain-security-1]: https://drive.google.com/file/d/1aXJgpGs6TznOx5uO7U1cvkvi-zVEjPSJ/view
[from-atom-to-sublime]: https://parsiya.net/blog/2017-07-08-from-atom-to-sublime-text/
[chroma]: https://github.com/alecthomas/chroma

<!-- End Links -->