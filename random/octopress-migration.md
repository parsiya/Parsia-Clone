---
draft: false
toc: false
comments: false
categories:
- Random
tags:
- Hugo
- Octopress
title: "Migration from Octopress to Hugo"
wip: false
snippet: "Random scripts used to convert my Octopress blog to [Hugo](https://gohugo.io/), [blog posts](https://parsiya.net/categories/migration-to-hugo/)."
---

# Migration from Octopress to Hugo
Read about it here: https://parsiya.net/blog/2016-02-02-from-octopress-to-hugo/

## For the original imgcap
what it should have been

``` bash
sed -i -- 's/{% imgcap \([^ ]*\) \(.*\) %}/{{</* imgcap src="\1" caption="\2" */>}}/' *.markdown

sed -i -- 's/{% imgpopup \([^ ]*\) [^ ]* \(.*\) >}}/{{</* imgcap src="\1" caption="\2" */>}}/' *.markdown

sed -i -- 's/{% codeblock lang:\([^ ]*\) \(.*\) >}}/{{</* codecaption lang="\1" title="\2" */>}}/' *.markdown

{% codeblock lang:bash creating our root CA >}}

{{</* codecaption lang="csharp" title="RemotingLibrary.cs" */>}}

s3cmd sync --delete-removed -P . s3://$BUCKET_NAME

s3cmd sync --acl-public --delete-removed -MP --rr public/ s3://parsiya.io && s3cmd --acl-public --no-preserve --mime-type="text/css" put public/css/hugo-octopress.css s3://parsiya.io/css/hugo-octopress.css

s3cmd --acl-public --no-preserve --mime-type="text/css" put public/css/octo1.css s3://parsiya.io/css/octo1.css

parsiya.io.s3-website-us-east-1.amazonaws.com

ns-1472.awsdns-56.org
ns-1922.awsdns-48.co.uk
ns-978.awsdns-58.net
ns-57.awsdns-07.com

s3cmd sync --acl-public --delete-removed -MP --rr public/ s3://parsiya.net && s3cmd --acl-public --no-preserve --mime-type="text/css" put public/css/hugo-octopress.css s3://parsiya.net/css/hugo-octopress.css

rd /q public
hugo
python s3cmd sync --acl-public --delete-removed -MP --rr public/ s3://parsiya.net
python s3cmd --acl-public --no-preserve --mime-type="text/css" put public/css/hugo-octopress.css s3://parsiya.net/css/hugo-octopress.css
rd /q public
```
