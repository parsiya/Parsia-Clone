---
draft: false
toc: false
comments: false
categories:
- Abandoned Research
title: "Learning Triton"
wip: false
snippet: "Notes on [Triton](https://triton.quarkslab.com/) installation."

---

So I decided to look at [Triton][triton-link].

#### Installation
I am going to talk about installation on my Debian VM.

According to [documentation][installation-link], in order to compile Triton we have to install the following libraries:

* libboost >= 1.58
* libpython 2.7.x
* libz3
* libcapstone >= 3.0
* Pin (optional) 71313

`libboost` and `libpython` can be install with:

    sudo apt-get install libboost-all-dev

`libz3` can be downloaded from [Github][z3-github] and then built:

    python scripts/mk_make.py
    cd build
    make
    sudo make install

The build process will take sometime but the compiled binaries can be downloaded from the [release][z3-release] page.

deb installers for `libcapstone` can be downloaded from here: https://www.capstone-engine.org/download/3.0.4/ubuntu-14.04/.

    wget http://www.capstone-engine.org/download/3.0.4/ubuntu-14.04/libcapstone3_3.0.4-0.1ubuntu1_amd64.deb
    wget http://www.capstone-engine.org/download/3.0.4/ubuntu-14.04/libcapstone-dev_3.0.4-0.1ubuntu1_amd64.deb

`Pin` can be downloaded from here: https://software.intel.com/en-us/articles/pintool-downloads

    wget http://software.intel.com/sites/landingpage/pintool/downloads/pin-2.14-71313-gcc.4.4.7-linux.tar.gz
    tar zxf pin-2.14-71313-gcc.4.4.7-linux.tar.gz

Need `cmake` so `sudo apt-get install cmake`.

[triton-link]: https://triton.quarkslab.com/
[installation-link]: http://triton.quarkslab.com/documentation/doxygen/#install_sec
[z3-release]: https://github.com/Z3Prover/z3/releases
[z3-github]: https://github.com/Z3Prover/z3/releases
[capstone-github]: https://github.com/aquynh/capstone.git
