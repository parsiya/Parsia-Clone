---
draft: false
toc: true
comments: false
categories:
- Research
title: "Comparing some SAST and DAST solutions."
wip: false
snippet: "Comparing the solutions I've worked with."
---

This is something I created to explain my experience with these tools personally
and professionally. These are my personal opinions. If I don't like your product
I can change my mind with a six figure bribe, lol.

## DAST

| Name | Pros | Cons |
|-|-|-|
| Burp Standard | <ul><li>Everyone is familiar with it</li><li>Customizable, many extensions</li><li>Lots of 3rd party materials</li><li>Reasonable price</li></ul> | <ul><li>Mostly great for manual scans</li><li>Not that great in the CI/CD pipeline</li></ul> |
| Nuclei | <ul><li>FOSS</li><li>Many community templates for CVEs</li><li>Easy to use, fire and forget</li><li>Easy to write templates</li></ul> | <ul><li>Template logic is simple</li><li>Supports steps but needs manual config</li><li>Mostly used for unauthenticated scans</li></ul> |
| ZAP | <ul><li>FOSS</li><li>Industry standard</li><li>Many tutorials</li></ul>  | <ul><li>Auth config is hard</li><li>Had to write custom code for integration</li><li>Funding issues</li></ul> |

### DAST Notes

1. Burp has an enterprise version that is supposedly better for pipelines. I have never used it. It's a solid tool, regardless.

## SAST
Keep in mind that I am a Semgrep junkie! I don't work for them.

| Name | Pros | Cons |
|-|-|-|
| CodeQL | <ul><li>Integrated with GitHub</li><li>Powerful Analysis</li><li>Can reuse the database for further analysis</li></ul> | <ul><li>Needs buildable code</li><li>Licensing :(</li><li>Rules are complex and not for devs</li><li>GitHub is a 1st class citizen for support and features</li></ul> |
| Semgrep | <ul><li>FOSS scanner</li><li>Lots of free rules</li><li>Easy rule syntax (good for devs)</li><li>Integration with many CI/CD platforms</li><li>Secret Scanning + validation</li><li>Supply chain + reachability analysis</li></ul> | <ul><li>Free rules are just OK</li><li>Need custom rules to be effective</li><li>Supply chain + secret scanning is paid</li><li>No inter-file analysis in free version</li></ul> |

### SAST Notes

1. CodeQL needs you to pay for GitHub advanced security (for private repos)
   which also has support for supply chain (Dependabot) and secret scanning +
   validation. I am not sure if CodeQL is used for those, but you get everything
   as a bundle when you pay for it.
2. I've not used the Semgrep supply chain and reachability analysis.

<!-- <ul><li>A</li><li>B</li><li>C</li><li>D</li></ul>  -->
