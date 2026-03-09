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

How this is deployed/created:

* Current: [Automagically Deploying Websites with Custom Domains to GitHub Pages][github-pages-custom-domain]
* Old: [Deploying my Knowledge Base at parsiya.io to S3 with Travis CI][deploying-with-travis]
* [Semi-Automated Cloning: Pain-Free Knowledge Base Creation][semi-automated]

[github-pages-custom-domain]: https://parsiya.net/blog/2021-02-17-automagically-deploying-websites-with-custom-domains-to-github-pages/
[semi-automated]: https://parsiya.net/blog/2018-04-24-semi-automated-cloning-pain-free-knowledge-base-creation/
[deploying-with-travis]: https://parsiya.net/blog/2018-04-24-deploying-my-knowledge-base-at-parsiya.io-to-s3-with-travis-ci/

# AI Usage
This repository includes a few GitHub Copilot customizations in `.github/`.

* [.github/instructions/markdown.instructions.md](.github/instructions/markdown.instructions.md)
	These apply when editing Markdown and capture the repository's formatting
	rules.
* A `refine` skill in [.github/skills/refine/SKILL.md](.github/skills/refine/SKILL.md)
	Invoke it from Copilot Chat with `/refine`.

What `refine` does:

* Proofreads Markdown.
* Fixes punctuation, typos, misspellings, grammar, and similar surface-level
	issues.
* Preserves voice and structure.
* Keeps edits scoped to what was requested instead of rewriting aggressively.

### How to Use

1. In VS Code, highlight the part you want to edit.
2. Type `/refine` in GitHub Copilot Chat's window.

# Content License
Except where otherwise noted, non-code material on this website is licensed under
a <a rel="license" target="_blank" href="https://creativecommons.org/licenses/by-nc/4.0/">Creative Commons BY-NC</a>.
