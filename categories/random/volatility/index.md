---
draft: false
toc: false
comments: false
categories:
- Random
tags:
- Volatility
- Forensics
title: "Volatility on Windows Notes"
wip: false
snippet: "Using Volatility on Windows."
---

# rekal
http://blog.rekall-forensic.com/2014/10/vm-discovery-and-introspection-with.html

```
rekal -v live
```
## vmscan
Admin cmd will not work because virtualbox is running as normal user?

```
$ VBoxManage.exe list runningvms

$ VBoxManage debugvm "Debian3 Clone" dumpvmcore --filename e:\test1
```

```
uname -r
3.16.0-4-amd64

cat /etc/*-release
Debian GNU/Linux 8 (Jessie)
```

# Volatility
Volatility Standalone Windows does not have Linux profiles, copy them all to a directory called `profiles` and load them with `--plugins=profiles`.

Download profiles:

* https://github.com/volatilityfoundation/profiles
* https://github.com/volatilityfoundation/volatility/wiki/Linux#making-the-profile

Then run

* `vol.exe --plugins=profiles --info | findstr Linux`

to get the profile name.

Then run the profile manually

* `vol.exe --plugins=profiles --profile=LinuxDebian8x64 -f test1 imagecopy -O test2.raw`

Output file is around 4GBs.

```
E:\volatility_2.6_win64_standalone>vol.exe --plugins=profiles --profile=LinuxDebian8x64 -f test2.raw truecryptsummary
Volatility Foundation Volatility Framework 2.6
ERROR   : volatility.debug    : This command does not support the profile LinuxDebian8x64

LinuxAMD64PagedMemory

AMD64PagedMemory
```

## Plugins?

* `truecryptmaster`: Recover TrueCrypt 7.1a Master Keys
* `truecryptpassphrase`: TrueCrypt Cached Passphrase Finder
* `truecryptsummary`: TrueCrypt Summary

# Swap Digger
Swap digger to get Linux password from swap file:

* https://github.com/sevagas/swap_digger