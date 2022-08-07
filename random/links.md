---
draft: false
toc: true
comments: false
categories:
- Random
tags:
- links
title: "Random Links"
wip: true
snippet: "This is my random list of (mostly security) links."
---

# Go

* Web Assembly and Go: A look to the future
    * https://brianketelsen.com/web-assembly-and-go-a-look-to-the-future/
* Go 1.11: WebAssembly for the gophers
    * https://medium.zenika.com/go-1-11-webassembly-for-the-gophers-ae4bb8b1ee03
* Using Interfaces and Dependency Injection to Future Proof Your Designs
    * https://medium.com/dm03514-tech-blog/you-are-going-to-need-it-using-interfaces-and-dependency-injection-to-future-proof-your-designs-2cf6f58db192
* Taking Go modules for a spin
    * https://dave.cheney.net/2018/07/14/taking-go-modules-for-a-spin
* How to build RPC server in golang
    * https://parthdesai.me/articles/2016/05/20/go-rpc-server/
* one-file-pdf - A minimalist PDF generator
    * https://github.com/balacode/one-file-pdf
* Introduction to Go Modules
    * https://roberto.selbach.ca/intro-to-go-modules/
* Tracking down a Golang memory leak with grmon
    * https://medium.com/@KentGruber/tracking-down-a-golang-memory-leak-with-grmon-74569a00a177
* Using Go modules with vendor support on Travis CI
    * https://arslan.io/2018/08/26/using-go-modules-with-vendor-support-on-travis-ci/
* A quick one-liner to list all imports of your current project
    * https://www.reddit.com/r/golang/comments/8cl6jb/a_quick_oneliner_to_list_all_imports_of_your/
    * `go list -json . | jq .Imports,.TestImports | sort | uniq | tail -n +3`
* Go Compiler Internals
    * https://eli.thegreenplace.net/2019/go-compiler-internals-adding-a-new-statement-to-go-part-1/
    * https://eli.thegreenplace.net/2019/go-compiler-internals-adding-a-new-statement-to-go-part-2/
* goebpf - Library to work with eBPF programs from Go
    * https://github.com/dropbox/goebpf
* script - Making it easy to write shell-like scripts in Go
    * https://github.com/bitfield/script
* llvm: Library for interacting with LLVM IR in pure Go
    * https://github.com/llir/llvm

# .NET

* Tools for Exploring .NET Internals
    * https://mattwarren.org/2018/06/15/Tools-for-Exploring-.NET-Internals/
* Resources for Learning about .NET Internals
    * https://mattwarren.org/2018/01/22/Resources-for-Learning-about-.NET-Internals/
* Introducing .NET Core 2.1 Flagship Types: Span T and Memory T
    * https://www.codemag.com/Article/1807051/Introducing-.NET-Core-2.1-Flagship-Types-Span-T-and-Memory-T
* Detecting Malicious Use of .NET
    1. https://countercept.com/blog/detecting-malicious-use-of-net-part-1/
    2. https://countercept.com/blog/detecting-malicious-use-of-net-part-2/
* Fuzzing the .NET JIT Compiler
    * https://mattwarren.org/2018/08/28/Fuzzing-the-.NET-JIT-Compiler/

# Tools

* Mallet, a framework for creating proxies
    * https://sensepost.com/blog/2018/mallet-a-framework-for-creating-proxies/
* House: A Mobile Analysis Platform Built on Frida
    * https://github.com/nccgroup/house
* Socks proxy server using PowerShell
    * https://github.com/p3nt4/Invoke-SocksProxy
* BeRoot: Privilege Escalation Project - Windows / Linux / Mac
    * https://github.com/AlessandroZ/BeRoot
* DbgShell: A PowerShell front-end for the Windows debugger engine
    * https://github.com/Microsoft/DbgShell
* SleuthQL: - Burp History parsing tool to discover potential SQL injection points
    * https://github.com/RhinoSecurityLabs/SleuthQL
* ExchangeRelayX: An NTLM relay tool to the EWS endpoint for on-premise exchange servers
    * https://github.com/quickbreach/ExchangeRelayX
* windows-acl: working with ACLs in Rust
    * https://blog.trailofbits.com/2018/08/23/introducing-windows-acl-working-with-acls-in-rust/
* Notable: Note taking app
    * https://github.com/jmcfarlane/notable
* TCPHound: Win32 utility for auditing TCP connections
    * https://github.com/limbenjamin/TCPHound
* PolarProxy is a transparent TLS proxy that creates PCAP files with the decrypted data.
    * https://www.netresec.com/?page=PolarProxy
* InfinityHook: Hook system calls, context switches, page faults and more.
    * https://github.com/everdox/InfinityHook
* Fermion, an electron wrapper for Frida & Monaco.
    * https://github.com/FuzzySecurity/Fermion
* pown-cdb: Automate common Chrome Debug Protocol tasks to help debug web applications from the command-line
    * https://github.com/pownjs/pown-cdb
* VS Code x Frida
    * https://github.com/chichou/vscode-frida
* burptime: Burp Show Response Time.
    * https://github.com/virusdefender/burptime
* Example of using Turbo Intruder in a "listen and attack" mode.
    * https://gist.github.com/defparam/840f7d9e31f77b3c5460c5921e0787ef
* Dead code elimination with Triton
    * https://github.com/JonathanSalwan/Triton/issues/1130

# Static Analysis

* Static Program Analysis book (updated regularly)
    * https://cs.au.dk/~amoeller/spa/spa.pdf
* ShellCheck, a static analysis tool for shell scripts
    * https://github.com/koalaman/shellcheck
* Security Code Audit - For Fun and Fails
    * https://frycos.github.io/vulns4free/2022/05/24/security-code-audit-fails.html
* Horde Webmail - Remote Code Execution via Email - PHP Static Analysis guide
    * https://blog.sonarsource.com/horde-webmail-rce-via-email/
* Shells.Systems - static code analysis archive
    * https://shells.systems/category/static-code-analysis/

# Cloud

* AWS Privilege Escalation – Methods and Mitigation
    * https://rhinosecuritylabs.com/aws/aws-privilege-escalation-methods-mitigation/
* Analysis of Netflix's Streaming Services Architecture
    * https://medium.com/swlh/a-design-analysis-of-cloud-based-microservices-architecture-at-netflix-98836b2da45f

# Mobile - IoT

* Learning Bluetooth Hackery with BLE CTF
    * http://www.hackgnar.com/2018/06/learning-bluetooth-hackery-with-ble-ctf.html
* Giving Yourself a Window to Debug a Shared Library Before DT_INIT – with Frida, on Android
    * http://www.giovanni-rocca.com/giving-yourself-a-window-to-debug-a-shared-library-before-dt_init-with-frida-on-android/
* Getting started with Firmware Emulation for IoT Devices
    * https://blog.attify.com/getting-started-with-firmware-emulation/
* Patching Binaries with Radare2 – ARM64
    * https://scriptdotsh.com/index.php/2018/08/13/reverse-engineering-patching-binaries-with-radare2-arm-aarch64/
* Independent Security Evaluators IoT Writeups
    * https://blog.securityevaluators.com/iselabs/home
* Let’s write Swift code to intercept SSL Pinning HTTPS Requests
    * https://medium.com/@kennethpoon/lets-write-swift-code-to-intercept-ssl-pinning-https-requests-12446303cc9d
* Android CrackMes
    * https://github.com/reoky/android-crackme-challenge
* Defeating an Android Packer with Frida
    * https://www.fortinet.com/blog/threat-research/defeating-an-android-packer-with-frida.html
* Frida-onload: Frida module to hook module initializations on Android
    * https://github.com/iGio90/frida-onload
* The Path to the Payload - Android Edition - Recon 2019
    * https://github.com/maddiestone/ConPresentations/blob/master/REcon2019.PathToThePayload.pdf
* SafetyNet Killer - a Frida script to bypass SafetyNet attestation
    * https://github.com/iGio90/SNetKiller
* Bypassing Certificate Pinning on iOS 12 with Frida
    * https://medium.com/@macho_reverser/bypassing-certificate-pinning-on-ios-12-with-frida-809acdb875e7
* Breaking mobile userland w[0x42]alls - Giovanni - iGio90 - Rocca
    * https://drive.google.com/file/d/1HwG6Ks_2dO0ut2plyPx1-svfNVKL1Mhu/view
* Skiptracing: Reversing Spotify.app
    * https://medium.com/@lerner98/skiptracing-reversing-spotify-app-3a6df367287d
* Reverse Engineering the iClicker Base Station
    * https://blog.ammaraskar.com/iclicker-reverse-engineering/
* Calling iOS Native Functions from Python Using Frida and RPC
    * https://grepharder.github.io/blog/0x04_calling_ios_native_functions_from_python_using_frida_and_rpc.html
* UCT - IMEI number disclosure through a text file
    * https://bugs.chromium.org/p/apvi/issues/detail?id=89&q=&can=1

# CTF

* Collections of 150 CTF Challenges (Vulnhub+HTB)
    * http://www.hackingarticles.in/capture-flag-challenges/
* Google's Beginner CTF
    * https://capturetheflag.withgoogle.com/#beginners/
* Small CTF challenges running on Docker
    * https://github.com/gabemarshall/microctfs
* CTF Series : Vulnerable Machines
    * https://bitvijays.github.io/LFC-VulnerableMachines.html
* Dockerscan: Docker Security Analysis Tools
    * https://github.com/cr0hn/dockerscan
* Defcon DFIR CTF 2018
    * https://defcon2018.ctfd.io/

# Netsec

* Recon-ng Tutorial
    1. Install and Setup: https://securenetworkmanagement.com/recon-ng-tutorial-part-1/
    2. Workspaces and Import: https://securenetworkmanagement.com/recon-ng-tutorial-part-2/
    3. Usage and Reporting: https://securenetworkmanagement.com/recon-ng-tutorial-part-3/
* Command Injection/Shell Injection
    * https://www.exploit-db.com/docs/english/42593-command-injection---shell-injection.pdf
* Transferring Files from Linux to Windows (post-exploitation)
    * https://blog.ropnop.com/transferring-files-from-kali-to-windows/
* Building Autonomous AppSec Pipelines with the Robot Framework
    * https://github.com/we45/defcon26
* David Weston - Zer0ing Trust - Do Zero Trust Approaches Deliver Real Security
    * https://github.com/dwizzzle/Presentations/blob/master/David%20Weston%20-%20Zer0ing%20Trust%20-%20Do%20Zero%20Trust%20Approaches%20Deliver%20Real%20Security.pdf
* OSCP Journey: Exam & Lab Prep Tips
    * https://h4ck.co/oscp-journey-exam-lab-prep-tips/
* How to write an Nmap script
    * https://www.peerlyst.com/posts/how-to-write-an-nmap-script-chiheb-chebbi
* Bloodhound Walkthrough. A Tool for Many Tradecrafts
    * https://www.pentestpartners.com/security-blog/bloodhound-walkthrough-a-tool-for-many-tradecrafts/
* Understanding UNC paths, SMB, and WebDAV
    * https://www.n00py.io/2019/06/understanding-unc-paths-smb-and-webdav/
* Video: nmap Service Detection Customization
    * https://isc.sans.edu/diary/24970
* How masscan works
    * https://rushter.com/blog/how-masscan-works/

# Not Security

* Dealing with Hard Problems
    * https://artofproblemsolving.com/articles/hard-problems
* Generation of diagram and flowchart from text in a similar manner as markdown
    * https://github.com/knsv/mermaid
    * VS code preview: https://github.com/vstirbu/vscode-mermaid-preview
* Zotero: An open-source tool to help collect, organize, cite, and share research
    * https://www.zotero.org/
* How to Learn Anything... Fast - Josh Kaufman
    * https://www.youtube.com/watch?v=EtJy69cEOtQ

# *nix

* Intercepting and Emulating Linux System Calls with Ptrace
    * https://nullprogram.com/blog/2018/06/23/
* Sed - An Introduction and Tutorial
    * http://www.grymoire.com/Unix/sed.html
* Compiling DLLs with MinGW on Kali
    * https://blog.didierstevens.com/2018/07/10/quickpost-compiling-dlls-with-mingw-on-kali/
* How hostname to IP address Conversion or Name Resolution works in Linux?
    * https://javarevisited.blogspot.com/2017/04/how-hostname-to-ip-address-conversion-or-name-resolution-works-in-Linux.html
* Lin.security – practice your Linux privilege escalation foo
    * https://in.security/lin-security-practise-your-linux-privilege-escalation-foo/
* Replace a string with a new one in all files using sed and xargs
    * https://totallynoob.com/replace-a-string-with-a-new-one-in-all-files-using-sed-and-xargs/

# Windows

* Windows Privilege Escalation Methods for Pentesters
    * https://pentest.blog/windows-privilege-escalation-methods-for-pentesters/
* System call dispatching on Windows ARM64
    * https://gracefulbits.com/2018/07/26/system-call-dispatching-for-windows-on-arm64/
* Juicy Potato, Local Privilege Escalation tool from a Windows Service Accounts to SYSTEM
    * https://ohpe.github.io/juicy-potato/
* You can't contain me!: Analyzing and Exploiting an Elevation of Privilege Vulnerability in Docker for Windows
    * https://srcincite.io/blog/2018/08/31/you-cant-contain-me-analyzing-and-exploiting-an-elevation-of-privilege-in-docker-for-windows.html
* About WriteProcessMemory
    * https://theevilbit.blogspot.com/2018/08/about-writeprocessmemory.html
* Triaging a DLL planting vulnerability
    * https://blogs.technet.microsoft.com/srd/2018/04/04/triaging-a-dll-planting-vulnerability/
* Watch your Downloads: the risk of the "auto-download" feature on Microsoft Edge and Google Chrome
    * http://justhaifei1.blogspot.com/2015/10/watch-your-downloads-risk-of-auto.html
* Fix Windows 10 Privacy
    * https://fix10.isleaked.com/
* The Art of Becoming TrustedInstaller - Task Scheduler Edition
    * https://tyranidslair.blogspot.com/2019/09/the-art-of-becoming-trustedinstaller.html
* Modern Windows Attacks and Defense Lab
    * https://github.com/jaredhaight/WindowsAttackAndDefenseLab
* Spying on HTTPS - How Antivirus apps monitor HTTPs
    * https://textslashplain.com/2019/08/11/spying-on-https/
* An In Depth Tutorial on Linux Development on Windows with WSL and Visual Studio Code
    * https://devblogs.microsoft.com/commandline/an-in-depth-tutorial-on-linux-development-on-windows-with-wsl-and-visual-studio-code/
* [How To] Identify File Types in Windows
    * https://www.youtube.com/watch?v=-vsfm1IqmWA
* CVE-2019–13142: Razer Surround Elevation of Privilege
    * https://posts.specterops.io/cve-2019-13142-razer-surround-1-1-63-0-eop-f18c52b8be0c
* Executing Code Using Microsoft Teams Updater
    * https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/executing-code-using-microsoft-teams-updater/
* Windows API Hooking
    * https://ired.team/offensive-security/code-injection-process-injection/how-to-hook-windows-api-using-c++
* How to Transfer and Share Files Between Windows and Linux
    * https://www.makeuseof.com/tag/transfer-share-files-windows-linux/
* Deobfuscating Powershell Scripts
    * https://securityliterate.com/malware-analysis-in-5-minutes-deobfuscating-powershell-scripts/
* "whoami /priv" - Hack in Paris 2019
    * https://github.com/decoder-it/whoami-priv-Hackinparis2019/blob/master/whoamiprivParis_Split.pdf
* Sysmon 10 - New features including DNS monitoring
    * https://medium.com/@olafhartong/sysmon-10-0-new-features-and-changes-e82106f2e00
* Hunting COM Objects
    * Part 1: https://www.fireeye.com/blog/threat-research/2019/06/hunting-com-objects.html
    * Part 2: https://www.fireeye.com/blog/threat-research/2019/06/hunting-com-objects-part-two.html
* Hello World - Compiling Executables for the Classic POSIX Subsystem on Windows
    * https://blog.ret2.io/2017/09/20/subsystem-posix/
* 1-click RCE with Skype Web Plugin and QT apps
    * https://0x41.cf/infosec/2019/05/28/skype-web-plugin-ez-rce.html
* Windows 10 - Task Scheduler service - Privilege Escalation/Persistence through DLL planting
    * https://remoteawesomethoughts.blogspot.com/2019/05/windows-10-task-schedulerservice.html
* Windows NamedPipes 101 + Privilege Escalation
    * https://ired.team/offensive-security/privilege-escalation/windows-namedpipes-privilege-escalation
* DLL Import Redirection in Windows 10 1909
    * https://www.tiraniddo.dev/2020/02/dll-import-redirection-in-windows-10_8.html
* Debug C++ applications inside the Windows Subsystem for Linux using Visual Studio Code
    * https://code.visualstudio.com/docs/cpp/config-wsl
* CVE-2020-0668 - A Trivial Privilege Escalation Bug in Windows Service Tracing
    * https://itm4n.github.io/cve-2020-0668-windows-service-tracing-eop/
* See the command line of processes in task manager
    * https://twitter.com/flakpaket/status/1529839888471924738
* A History of MS-RPC and open source equivalents
    * https://kganugapati.wordpress.com/tag/msrpc/
* Offensive Windows IPC Internals 1: Named Pipes
    * https://csandker.io/2021/01/10/Offensive-Windows-IPC-1-NamedPipes.html
* Offensive Windows IPC Internals 2: RPC
    * https://csandker.io/2021/02/21/Offensive-Windows-IPC-2-RPC.html
* Offensive Windows IPC Internals 3: ALPC
    * https://csandker.io/2022/05/24/Offensive-Windows-IPC-3-ALPC.html
* Debugging and Reversing ALPC
    * https://csandker.io/2022/05/29/Debugging-And-Reversing-ALPC.html
* Windows Defender Internals
    * https://github.com/commial/experiments/tree/master/windows-defender
* CVE-2022-26937: Microsoft Windows Network File System NLM Portmap Stack Buffer Overflow
    * https://www.zerodayinitiative.com/blog/2022/6/7/cve-2022-26937-microsoft-windows-network-file-system-nlm-portmap-stack-buffer-overflow
* Chromium: Web Share API allows to write in UNC paths and/or in C:/Users/<username>/AppData/Local/Temp/ on Windows
    * https://bugs.chromium.org/p/chromium/issues/detail?id=1301920

# Reverse Engineering

* Reverse Engineering for Beginners
    * https://www.begin.re/
* How I Turn Frick into a Real Frida Based Debugger
    * http://www.giovanni-rocca.com/how-i-turn-frick-into-a-real-frida-based-debugger/
* Beginner Malware Reversing Challenges
    * https://www.malwaretech.com/beginner-malware-reversing-challenges
* x86 In-Depth 3: Identifying C-Style Structs
    * https://www.youtube.com/watch?v=WaH-aqQ15Xg
* x86 In-Depth 4: Labeling Structs Properly in IDA Pro
    * https://www.youtube.com/watch?v=X3xCwNt2ZVY
* Infected PDF: Extract the payload
    * https://www.adlice.com/infected-pdf-extract-payload/
* Solving the Atredis BlackHat 2018 CTF Challenge
    * http://www.msreverseengineering.com/blog/2018/7/24/the-atredis-blackhat-2018-ctf-challenge
* Tools for instrumenting Windows Defender's mpengine.dll
    * https://github.com/0xAlexei/WindowsDefenderTools
* Fast Incident Response: Tracking app
    * https://github.com/certsocietegenerale/FIR
* Reflective DLL Injection
    * https://0x00sec.org/t/reflective-dll-injection/3080
* Becoming a "Full-Stack Reverse Engineer" in three years
    * Slides: https://docs.google.com/presentation/d/1HLVUfbn9w7BXzYI437vF-yxEqujwLQp9brdIHhgTEv0/
    * Youtube: https://www.youtube.com/watch?v=9vKG8-TnawY
* Reverse engineering the rendering of The Witcher 3
    * Witcher tricks slides: https://drive.google.com/drive/folders/1gmn5XSYDUsOPXXKQO73zCpGAHWAfnK1U
    1. Tonemapping: https://astralcode.blogspot.com/2017/09/reverse-engineering-rendering-of.html
    2. Eye adaptation: https://astralcode.blogspot.com/2017/10/reverse-engineering-rendering-of.html
    3. Chromatic aberration: https://astralcode.blogspot.com/2017/10/reverse-engineering-rendering-of_26.html
    4. Vignette: https://astralcode.blogspot.com/2018/02/reverse-engineering-rendering-of.html
    5. Drunk effect: https://astralcode.blogspot.com/2018/08/reverse-engineering-rendering-of.html
* Behind Enemy Lines- Reverse Engineering C++ in Modern Ages
    * https://drive.google.com/file/d/1PgK-gWSgq48oVWQE7borOQHG4rpdmt60/view
* COM Hijacking Techniques David Tulis - DerbyCon 2019
    * https://www.youtube.com/watch?v=pH14BvUiTLY
* WinDbg commands flash cards
    * https://quizlet.com/12323606/windbg-commands-flash-cards/
* "Modern Debugging with WinDbg Preview" DEFCON 27 workshop
    * https://github.com/hugsy/defcon_27_windbg_workshop
    * WinDbg cheatsheet: https://github.com/hugsy/defcon_27_windbg_workshop/blob/master/windbg_cheatsheet.md
* Analysing RPC With Ghidra and Neo4j
    * https://blog.xpnsec.com/analysing-rpc-with-ghidra-neo4j/
* Trusted types & the end of DOM XSS - Krzysztof Kotowicz - LocoMocoSec 2019
    * https://www.youtube.com/watch?v=po6GumtHRmU
* Malware Unicorn RE workshops
    * https://malwareunicorn.org/#/workshops
* Electronegativity - Electron security checks
    * https://github.com/doyensec/electronegativity
* Overcoming Fear: Reversing With Radare2 - Arnau Gamez Montolio
    * https://www.youtube.com/watch?v=317dNavABKo
    * https://conference.hitb.org/hitbsecconf2019ams/materials/D1T3%20-%20Reversing%20with%20Radare2%20-%20Arnau%20Gamez%20Montolio.pdf
* hm0x14 CTF: reversing a (not so simple) crackme
    * https://antonioparata.blogspot.com/2019/06/hm0x14-ctf-reversing-not-so-simple.html
* Ghidra Utilities for Analyzing PC Firmware
    * https://github.com/al3xtjames/ghidra-firmware-utils
* Implementing a New CPU Architecture for Ghidra 
    * Slides: https://docs.google.com/presentation/d/1b955DV2ii-Dgv6YR4kUrJtjGugEqXD3FffTHRfvVSYo/edit
    * Code: https://github.com/guedou/ghidra-processor-mep
* gdbghidra - a visual bridge between a GDB session and GHIDRA
    * https://github.com/Comsecuris/gdbghidra
* python-decompile3: Python decompiler for 3.7+
    * https://github.com/rocky/python-decompile3
* Dragon Dance - Binary code coverage visualizer plugin for Ghidra
    * https://github.com/0ffffffffh/dragondance
* Course materials for Advanced Binary Deobfuscation by NTT Secure Platform Laboratories
    * https://github.com/malrev/ABD
* Virtual Method Table for newbies
    * Part 1: https://littlemastermind.codes/2020/02/01/virtual-method-table-for-newbies/
    * Part 2: https://littlemastermind.codes/2020/02/01/virtual-method-table-for-newbies-2/
* Using OOAnalyzer to Reverse Engineer Object Oriented Code with Ghidra
    * https://insights.sei.cmu.edu/sei_blog/2019/07/using-ooanalyzer-to-reverse-engineer-object-oriented-code-with-ghidra.html
* Extending LLVM for Code Obfuscation
    * Part 1: https://www.praetorian.com/blog/extending-llvm-for-code-obfuscation-part-1
    * Part 2: https://www.praetorian.com/blog/extending-llvm-for-code-obfuscation-part-2
* Finding Bugs in Windows Drivers, Part 1 – WDM
    * https://www.cyberark.com/resources/threat-research-blog/finding-bugs-in-windows-drivers-part-1-wdm
* Hunting for Bugs in Windows Mini-Filter Drivers
    * https://googleprojectzero.blogspot.com/2021/01/hunting-for-bugs-in-windows-mini-filter.html
* Technical Dive: Reverse Engineering AOL 3.0
    * https://g.livejournal.com/12127.html

# Python

* CPython internals: A ten-hour codewalk through the Python interpreter source code
    * https://www.youtube.com/playlist?list=PLzV58Zm8FuBL6OAv1Yu6AwXZrnsFbbR0S
* Pyshark - Python Wrapper For Tshark, Allowing Python Packet Parsing Using Wireshark Dissectors 
    * https://www.kitploit.com/2019/08/pyshark-python-wrapper-for-tshark.html
* FOIA-ed NSA Python Course
    * https://archive.org/details/comp3321

# Websec

* Practical JSONP Injection
    * https://www.mohamedharon.com/2018/01/practical-jsonp-injection.html
* WebAssembly: potentials and pitfalls
    * https://www.forcepoint.com/blog/security-labs/webassembly-potentials-and-pitfalls
* Analyzing WebAssembly Binaries
    * https://www.forcepoint.com/blog/security-labs/analyzing-webassembly-binaries
* JWT Cheatsheet
    * https://assets.pentesterlab.com/jwt_security_cheatsheet/jwt_security_cheatsheet.pdf
* LDAP Injection Cheatsheet
    * https://www.checkmarx.com/knowledge/knowledgebase/LDAP
* vuLnDAP: vulnerable LDAP based web app
    * https://digi.ninja/projects/vulndap.php
* How to Hack WebSockets and Socket.io
    * https://www.blackhillsinfosec.com/how-to-hack-websockets-and-socket-io/
* JSON Web Token Best Current Practices
    * https://tools.ietf.org/html/draft-ietf-oauth-jwt-bcp-04
* The Illustrated TLS Connection
    * https://tls.ulfheim.net/
* OAuth 2.0 Security Best Current Practice
    * https://tools.ietf.org/html/draft-ietf-oauth-security-topics-13
* Automating local DTD discovery for XXE exploitation
    * https://www.gosecure.net/blog/2019/07/16/automating-local-dtd-discovery-for-xxe-exploitation
    * https://github.com/GoSecure/dtd-finder
* Jackson gadgets - Anatomy of a vulnerability - Java Deserialization
    * https://blog.doyensec.com/2019/07/22/jackson-gadgets.html
* Knife: A Burp extension that add some useful function to Context Menu
    * https://github.com/bit4woo/knife
* Better API Penetration Testing with Postman
    * https://blog.secureideas.com/2019/03/better-api-penetration-testing-with-postman-part-1.html
    * https://blog.secureideas.com/2019/03/better-api-penetration-testing-with-postman-part-2.html
    * https://blog.secureideas.com/2019/04/better-api-penetration-testing-with-postman-part-3.html
    * https://blog.secureideas.com/2019/06/better-api-penetration-testing-with-postman-part-4.html
* JavaScript Supply Chain Security - LocoMocoSec 2019
    * https://www.youtube.com/watch?v=HDo2iOlkbyc
* XXE: How to become a Jedi - Yaroslav Babin
    * https://www.slideshare.net/ssuserf09cba/xxe-how-to-become-a-jedi
* Java Serialization: A Practical Exploitation Guide
    * https://www.rapid7.com/research/report/exploiting-jsos/
* XML External Entity(XXE)
    * http://ghostlulz.com/xml-external-entityxxe/
* Exploiting XXE with local DTD files
    * https://mohemiv.com/all/exploiting-xxe-with-local-dtd-files/
* The parts of JWT security nobody talks about
    * https://pragmaticwebsecurity.com/talks/jwtsecurity.html
* Pro Tips: Testing Applications Using Burp, and More
    * https://www.coalfire.com/Solutions/Coalfire-Labs/The-Coalfire-LABS-Blog/june-2018/protips-testing-applications-using-burp-and-more
* Actual XSS in 2020
    * https://netsec.expert/2020/02/01/xss-in-2020.html
* XXE & SQLi In PaperThin CommonSpot CMS
    * https://www.aon.com/cyber-solutions/aon_cyber_labs/xxe-sqli-in-paperthin-commonspot-cms/
* OpenID Connect & OAuth 2.0 Security Best Practices
    * https://speakerdeck.com/leastprivilege/oauth-and-openid-connect-security-best-practices
* Reverb: speculative debugging for web applications
    * https://blog.acolyer.org/2020/01/27/reverb-speculative-debugging/
* Open redirect vulnerability and how to use it "correctly" in bug bounty
    * https://medium.com/@byq/from-open-redirect-to-rce-in-one-week-66a7f73fd082
* Arbitrary File Upload Tricks In Java
    * https://pyn3rd.github.io/2022/05/07/Arbitrary-File-Upload-Tricks-In-Java/
* Tag each request with the corresponding browser profile in Burp's embedded browser
    * https://twitter.com/MasteringBurp/status/1435176162611896322
* The Underrated Bugs, Clickjacking, CSS Injection, Drag-Drop XSS, Cookie Bomb, Login+Logout CSRF…
    * https://medium.com/@renwa/the-underrated-bugs-clickjacking-css-injection-drag-drop-xss-cookie-bomb-login-logout-csrf-84307a98fffa
* Critical SSRF on Evernote
    * https://blog.neolex.dev/13/
* GitLab: Steal private objects of other projects via project import
    * https://hackerone.com/reports/743953
* Apache Pinot SQLi & RCE Cheat Sheet
    * https://blog.doyensec.com/2022/06/09/apache-pinot-sqli-rce.html

# Misc

* Mainframe Hacking
    * https://www.youtube.com/playlist?list=PLBVy6TfEpKmGdX1OE_xjK0GKGjSLwxVn_
* Woot 2018: A Modern History of Offensive Security Research
    * https://docs.google.com/presentation/d/19HfkIojyLE8L8X8aZT-lJont96JqIg4PqEhb2juIK2c/
* Learning PowerShell
    * https://www.verboon.info/2018/03/its-never-too-late-to-start-learning-powershell/
* CrystalBall, Data Gathering and Machine Learning System for SAT Solvers
    * Blog: https://www.msoos.org/2019/06/crystalball-sat-solving-data-gathering-and-machine-learning/
    * Code: https://github.com/msoos/cryptominisat/tree/crystalball
    * Paper: https://www.msoos.org/wordpress/wp-content/uploads/2019/06/sat19-skm.pdf
* Beyond your studies: a presentation about job interviews by Ange Albertini
    * Youtube: https://www.youtube.com/watch?v=Prgv9pNvy24
    * Slides: https://speakerdeck.com/ange/beyond-your-studies
* Wireshark Tutorial: Examining Qakbot Infections
    * https://unit42.paloaltonetworks.com/tutorial-qakbot-infection/
* Alfa AWUS036ACH Kali Configuration Guide
    * https://forums.hak5.org/topic/43124-alfa-awus036ach-kali-configuration-guide/
* Resistance Isn't Futile: A Practical Approach to Threat Modeling
    * https://www.slideshare.net/KatieNickels/resistance-isnt-futile-a-practical-approach-to-threat-modeling
* Generate Railroad Diagrams from Regular Expressions
    * https://regexper.com/
* 10 useful websites
    * https://flourish.studio
    * https://mentimeter.com
    * https://Webwhiteboard.com
    * https://diagrams.net
    * https://Untools.co - Tools for better thinking
* Learning Machine Learning Part 1: Introduction and Revoke-Obfuscation
    * https://posts.specterops.io/learning-machine-learning-part-1-introduction-and-revoke-obfuscation-c73033184f0
* Learning Machine Learning Part 2: Attacking White Box Models
    * https://posts.specterops.io/learning-machine-learning-part-2-attacking-white-box-models-1a10bbb4a2ae
* Learning Machine Learning Part 3: Attacking Black Box Models
    * https://posts.specterops.io/learning-machine-learning-part-3-attacking-black-box-models-3efffc256909
* Formal Methods Only Solve Half My Problems
    * https://brooker.co.za/blog/2022/06/02/formal.html
* Installing a payphone in my house
    * https://bert.org/2022/06/02/payphone/
* Threat Modeling at Mercari
    * https://engineering.mercari.com/en/blog/entry/20220426-threat-modeling-at-mercari/
* Trail of Bits: CTF Field Guide
    * https://github.com/trailofbits/ctf

# Exploit Dev

* Return Oriented Programming Series
    * Introduction: https://tuonilabs.wordpress.com/2018/07/30/return-oriented-programming-series-introduction/
    * Setup: https://tuonilabs.wordpress.com/2018/07/30/rop-environment-setup/
    * Writeups: https://tuonilabs.wordpress.com/2018/07/31/rop-write-ups/
* Exploiting TurboFan Through Bounds Check Elimination
    * https://gts3.org/2019/turbofan-BCE-exploit.html
* HowTo: ExploitDev Fuzzing
    * https://hansesecure.de/2018/03/howto-exploitdev-fuzzing/
* Vulnerable C++ code for practice
    * https://github.com/atxsinn3r/VulnCases
* Finding and exploiting CVE-2018–7445 (unauthenticated RCE in MikroTik’s RouterOS SMB)
    * https://medium.com/@maxi./finding-and-exploiting-cve-2018-7445-f3103f163cc1
* Weird Machines, Exploitability, and Provable Unexploitability
    * https://ieeexplore.ieee.org/document/8226852
* Before you ship a "security mitigation" ... (related to the above)
    * http://addxorrol.blogspot.com/2020/03/before-you-ship-security-mitigation.html
* Zoom: Remote Code Execution with XMPP Stanza Smuggling
    * https://bugs.chromium.org/p/project-zero/issues/detail?id=2254
* Heap Binary Exploitation video
    * https://www.youtube.com/watch?v=Im1SqwOVsEQ
* Exploit Development: No Code Execution? No Problem! Living The Age of VBS, HVCI, and Kernel CFG
    * https://connormcgarr.github.io/hvci/
* libxml2: heap-buffer-overflow in xmlBufAdd
    * https://bugs.chromium.org/p/project-zero/issues/detail?id=2272
* Is Exploiting a Null Pointer Deref for LPE just a Pipe Dream?
    * CVE-2021-4198 and CVE-2021-4199 in Bit Defender via Named Pipes
    * https://www.zerodayinitiative.com/blog/2022/6/1/is-exploiting-a-null-pointer-deref-for-lpe-just-a-pipe-dream
* HEVD - UAF NONPAGEDNX Vulnerability
    * https://github.com/vportal/HEVD
* The AMD Branch (Mis)predictor: Just Set it and Forget it!
    * https://grsecurity.net/amd_branch_mispredictor_just_set_it_and_forget_it
* Introduction to VirtualBox security research
    * https://blog.doyensec.com/2022/04/26/vbox-fuzzing.html
* Linux kernel bug hunting/exploitation resources
    * https://twitter.com/alexjplaskett/status/1535189987846668288
    * Playing for K(H)eaps: Understanding and Improving Linux Kernel Exploit Reliability
        * https://www.usenix.org/system/files/sec22fall_zeng.pdf
    * Put an io_uring on it: Exploiting the Linux Kernel
        * https://www.graplsecurity.com/post/iou-ring-exploiting-the-linux-kernel
    * CVE-2022-0185 - Winning a $31337 Bounty after Pwning Ubuntu and Escaping Google's KCTF Containers
        * https://www.willsroot.io/2022/01/cve-2022-0185.html
    * syzkaller results
        * https://syzkaller.appspot.com/upstream
    * Exploitation Mitigations repo by NCC
        * https://github.com/nccgroup/exploit_mitigations
    * One day short of a full chain: Part 1 - Android Kernel arbitrary code execution - CodeQL
        * https://securitylab.github.com/research/one_day_short_of_a_fullchain_android/
    * Linux Kernel Exploitation
        * https://github.com/xairy/linux-kernel-exploitation
* PlayStation: bd-j exploit chain
    * https://hackerone.com/reports/1379975
* Exploration of the Dirty Pipe Vulnerability (CVE-2022-0847)
    * https://lolcads.github.io/posts/2022/06/dirty_pipe_cve_2022_0847/
* A Story of a Bug Found Fuzzing - Microsoft Edge
    * https://microsoftedge.github.io/edgevr/posts/a-story-of-a-bug-found-fuzzing/
* PS4/PS5 Blu-Ray attacks: TheFloW shares his presentation slides
    * https://wololo.net/2022/06/13/ps4-ps5-blu-ray-attacks-theflow-shares-his-presentation-slides/
* An Autopsy on a Zombie In-the-Wild 0-day
    * https://googleprojectzero.blogspot.com/2022/06/an-autopsy-on-zombie-in-wild-0-day.html
* Pwn2Own 2021 Canon ImageCLASS MF644Cdw writeup
    * https://doar-e.github.io/blog/2022/06/11/pwn2own-2021-canon-imageclass-mf644cdw-writeup/
* Reverse engineering x64 binaries with Radare2 - Bypasssing DEP with simple ROP Chains
    * https://artik.blue/reversing-radare-21

# C/C++

* Project Based Tutorials in C
    * https://github.com/rby90/Project-Based-Tutorials-in-C/
* C++ Russia 2021 - some talks are in English
    * https://www.youtube.com/playlist?list=PLZN9ZGiWZoZqIsJqUgmMznD68NSsyaAhy

# Blockchain

* Wireshark dissectors for Ethereum ÐEVp2p protocols
    * https://media.consensys.net/releasing-wireshark-dissectors-for-ethereum-%C3%B0%CE%BEvp2p-protocols-215c9656dd9c
* Using a Hardware Security Module with Hyperledger Fabric 1.2 SDK for Node.js
    * https://www.linkedin.com/pulse/using-hardware-security-module-hyperledger-fabric-12-sdk-girard/
* Fumblechain - A Purposefully Vulnerable Blockchain
    * https://research.kudelskisecurity.com/2019/07/25/introducing-fumblechain-a-purposefully-vulnerable-blockchain/
    * https://github.com/kudelskisecurity/fumblechain
* Mirror Protocol vulnerability:
    * https://twitter.com/FatManTerra/status/1529978941062139906
* Proxy Libraries in Solidity
    * https://blog.openzeppelin.com/proxy-libraries-in-solidity-79fbe4b970fd/
* List of Smart Contract Security Vulnerabilities
    * https://github.com/runtimeverification/verified-smart-contracts/wiki/List-of-Security-Vulnerabilities

# Cryptography

* A (relatively easy to understand) primer on elliptic curve cryptography
    * https://arstechnica.com/information-technology/2013/10/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography/
* A Decade of Lattice Cryptography
    * http://web.eecs.umich.edu/~cpeikert/pubs/lattice-survey.pdf
* Peter Gutmann's "godzilla crypto tutorial
    * https://www.cs.auckland.ac.nz/~pgut001/tutorial/index.html
* Estimating the Bit Security of Pairing-Friendly Curves
    * https://research.nccgroup.com/2022/02/03/estimating-the-bit-security-of-pairing-friendly-curves/

# CI/CD

* Driving OWASP @zaproxy using Selenium
    * https://www.facebook.com/OWASPLondon/videos/266758580490230/

# Docker

* Unprivileged Docker Builds – A Proof of Concept
    * https://zwischenzugs.com/2018/04/23/unprivileged-docker-builds-a-proof-of-concept/
* Understanding Docker container escapes
    * https://blog.trailofbits.com/2019/07/19/understanding-docker-container-escapes/
* Docker for Pentesters
    * https://blog.ropnop.com/docker-for-pentesters/
* Why is Exposing the Docker Socket a Really Bad Idea?
    * https://blog.quarkslab.com/why-is-exposing-the-docker-socket-a-really-bad-idea.html

# Fuzzing

* Fuzzing projects with American fuzzy lop (AFL)
    * https://0x00sec.org/t/fuzzing-projects-with-american-fuzzy-lop-afl/6498
* AFL-unicorn: What is it and how to use it?
    * https://tthtlc.wordpress.com/2019/03/16/afl-unicorn-what-is-it-and-how-to-use-it/amp/
* A Simple Tutorial of AFL-Fuzzer
    * http://spencerwuwu-blog.logdown.com/posts/1366733-a-simple-guide-of-afl-fuzzer
* FUZZING - AMERICAN FUZZY LOP, ADDRESS SANITIZER AND LIBFUZZER
    * https://int21.de/slides/auscert-fuzzing/#/
* Binary fuzzing strategies: what works, what doesn't by AFL creator
    * https://lcamtuf.blogspot.com/2014/08/binary-fuzzing-strategies-what-works.html
* Google Fuzzing repository
    * https://github.com/google/fuzzing
* Mindshare: Automated Bug Hunting by Modeling Vulnerable Code
    * https://www.zerodayinitiative.com/blog/2019/7/16/mindshare-automated-bug-hunting-by-modeling-vulnerable-code
* Putting the Hype in the Hypervisor - Brandon Falk
    * https://www.youtube.com/watch?v=4nz-7ktdU_k
* Microsoft lain fuzzing framework (in Rust)
    * https://github.com/microsoft/lain
* Grizzly: A cross-platform browser fuzzing framework
    * https://github.com/MozillaSecurity/grizzly
* Fuzzing the Kernel Using AFL-Unicorn
    * https://github.com/fgsect/unicorefuzz
* Provoking Browser Quirks With Behavioural Fuzzing
    * https://portswigger.net/research/provoking-browser-quirks-with-behavioural-fuzzing
* Windows Kernel Fuzzing for Intermediate Learners by Ben Nagy
    * https://github.com/bnagy/slides/blob/master/alpc_lowres.pdf
* RAF - Ruby ALPC Fuzzer
    * https://github.com/bnagy/raf
* Go tools for basic ALPC hacking.
    * https://github.com/bnagy/alpcgo
* High-Throughput, Formal-Methods-Assisted Fuzzing for LLVM
    * https://blog.regehr.org/archives/2148
* Fuzzing USB with Raw Gadget
    * Slides: https://docs.google.com/presentation/d/1sArf2cN5tAOaovlaL3KBPNDjYOk8P6tRrzfkclsbO_c/edit
    * Video: https://www.youtube.com/watch?v=OVbzlN3evzo&t=13589s
    * Tool: https://github.com/xairy/raw-gadget
* Domain-specific Fuzzing With Waypoints Using Fuzzfactory
    * https://www.c0d3xpl0it.com/2019/12/domain-specific-fuzzing-with-waypoints.html
* sfuzz: coverage-guided, emulation-based greybox fuzzer
    * https://seal9055.com/blog/fuzzing/sfuzz
    * https://github.com/seal9055/sfuzz
* A mini symbolic execution engine
    * https://kqueue.org/blog/2015/05/26/mini-mc/
* Introducing Fuzz Introspector, an OpenSSF Tool to Improve Fuzzing Coverage
    * https://openssf.org/blog/2022/06/09/introducing-fuzz-introspector-an-openssf-tool-to-improve-fuzzing-coverage/
* SnapFuzz: An Efficient Fuzzing Framework for Network Applications
    * https://arxiv.org/abs/2201.04048
    * https://github.com/srg-imperial/SnapFuzz-artefact

# Game Hacking

* Simple C++ DLL Injecting Source Code Tutorial
    * https://www.youtube.com/watch?v=PZLhlWUmMs0
* How to Reverse Engineer Save Game Files - Titan Quest Cheats
    * https://guidedhacking.com/threads/how-to-reverse-engineer-save-game-files-titan-quest-cheats.14469/
* GTA III; Money & Health Hacked
    * https://blog.th3-gr00t.tk/blog/notes/2022-05-30-GTA3-Money-Health-Hack/
* Exploiting the Wii U's USB Descriptor parsing
    * https://garyodernichts.blogspot.com/2022/06/exploiting-wii-us-usb-descriptor-parsing.html

# Documentation/Automation/Efficiency

* Documentation Writing for System Administrators - 2003
    * https://www.usenix.org/short-topics/documentation-writing-system-administrators
    * My notes: https://parsiya.net/blog/2020-02-06-documentation-writing-for-system-administrators-notes/
* Manual Work is a Bug
    * https://queue.acm.org/detail.cfm?id=3197520
    * Reflections on "Manual Work is a Bug": https://parsiya.net/blog/2018-10-03-reflections-on-manual-work-is-a-bug/
    * The Dark Side of "Manual Work is a Bug": https://parsiya.net/blog/2019-04-17-the-dark-side-of-manual-work-is-a-bug/
* Effective Engineer:
    * https://gist.github.com/rondy/af1dee1d28c02e9a225ae55da2674a6f
* From Idiot to Imposter: how to get started in a new field
    * https://www.emfcamp.org/schedule/2018/76-from-idiot-to-imposter-how-to-get-started-in-a-new-field
* GTD in 15 minutes – A Pragmatic Guide to Getting Things Done
    * https://hamberg.no/gtd
* How to write a BANGER blogpost! (Hacking the Google algorithm) - Fredrik "STÖK" Alexandersson
    * https://www.youtube.com/watch?v=nSykVNZLeOc&t=26841s

# Rust

* Rocketing to the moon with Rocket and Rust - how to write a backend web application in Rust using Rocket
    * https://geekmasher.dev/dev/rust/introduction-rust-rocket/
* Rust playground
    * https://typerust.dev/