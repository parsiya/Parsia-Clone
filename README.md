# Parsia Clone ![Deploy Clone](https://github.com/parsiya/parsia-clone/actions/workflows/gh-pages.yml/badge.svg)
This is my clone. I have been maintaining one internally at my work
(Cigital/Synopsys/Electronic Arts) since mid 2016. It has been decently
successful and well received. There is going to be some expected redundancy
between here and [parsiya.net][parsiya-net]. This repository will also contain
code and random notes that do not get published there, effectively removing the
Random-Code and Random-Notes repositories.

[parsiya-net]: https://parsiya.net

As of February 2021, the site is built with GitHub actions and hosted on GitHub
pages at [parsiya.io][parsiya-io].

[parsiya-io]: https://parsiya.io

## How this site is/was deployed/created:

* Current: [Automagically Deploying Websites with Custom Domains to GitHub Pages][github-pages-custom-domain]
* Old: [Deploying my Knowledge Base at parsiya.io to S3 with Travis CI][deploying-with-travis]
* [Semi-Automated Cloning: Pain-Free Knowledge Base Creation][semi-automated]

[github-pages-custom-domain]: https://parsiya.net/blog/2021-02-17-automagically-deploying-websites-with-custom-domains-to-github-pages/
[semi-automated]: https://parsiya.net/blog/2018-04-24-semi-automated-cloning-pain-free-knowledge-base-creation/
[deploying-with-travis]: https://parsiya.net/blog/2018-04-24-deploying-my-knowledge-base-at-parsiya.io-to-s3-with-travis-ci/

## Formatting
Using the [remark VS Code extension][remark] and a custom config in
[.remarkrc.mjs](.remarkrc.mjs).

[remark]: https://marketplace.visualstudio.com/items?itemName=unifiedjs.vscode-remark

## LLM Usage
LLM generated documents are clearly marked. I've not started adding LLM
generated content to this clone yet, but they will have a tag (**TODO**: update
this with a tag and the link when it's decided). The plan of how and what is
added is documented at my blog post [Manual Context is a Bug][man].

[man]: https://parsiya.net/blog/manual-context-is-a-bug/

## Content License
Except where otherwise noted, non-code material on this website is licensed under
a <a rel="license" target="_blank" href="https://creativecommons.org/licenses/by-nc/4.0/">Creative Commons BY-NC</a>.
