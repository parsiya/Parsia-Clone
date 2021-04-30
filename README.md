# Parsia Clone ![Deploy Clone](https://github.com/parsiya/parsia-clone/workflows/Deploy%20Blog/badge.svg)
This is my clone. I have been maintaining one internally at my work
(Cigital/Synopsys/Electronic Arts) since mid 2016. It has been decently
successful and well received. I have decided to make a public one. There is
going to be a lot of redundancy between here and [parsiya.net][parsiya-net] but
that is expected. This repository will also contain code and random notes that
do not get published there effectively removing the Random-Code and Random-Notes
repositories I recently started.

[parsiya-net]: https://parsiya.net

As of February 2021, the site is built with GitHub actions and hosted on GitHub
pages at [parsiya.io][parsiya-io].

[parsiya-io]: http://parsiya.io

How this is deployed/created:

* [Automagically Deploying Websites with Custom Domains to GitHub Pages][github-pages-custom-domain]
* [Deploying my Knowledge Base at parsiya.io to S3 with Travis CI][deploying-with-travis]
  * As of November 2020, I am using GitHub actions instead of Travis CI. See the
    [.github/workflows/deploy.yml](.github/workflows/deploy.yml) file for
    details. The old travis file is [.travis.yml](.travis.yml).
* [Semi-Automated Cloning: Pain-Free Knowledge Base Creation][semi-automated]

[github-pages-custom-domain]: https://parsiya.net/blog/2021-02-17-automagically-deploying-websites-with-custom-domains-to-github-pages/
[semi-automated]: https://parsiya.net/blog/2018-04-24-semi-automated-cloning-pain-free-knowledge-base-creation/
[deploying-with-travis]: https://parsiya.net/blog/2018-04-24-deploying-my-knowledge-base-at-parsiya.io-to-s3-with-travis-ci/

# Content License
Except where otherwise noted, non-code material on this website is licensed under
a <a rel="license" target="_blank" href="https://creativecommons.org/licenses/by-nc/4.0/">Creative Commons BY-NC</a>.
