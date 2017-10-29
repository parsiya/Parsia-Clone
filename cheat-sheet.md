Copy of [https://parsiya.net/cheatsheet/][cheat-sheet-ext].

# Contents

<!-- MarkdownTOC -->

- [Tar](#tar)
  - [Compressing a directory using tar](#compressing-a-directory-using-tar)
  - [Decompressing a tar.gz file](#decompressing-a-targz-file)
- [OpenSSL](#openssl)
  - [Dumping the TLS certificate using OpenSSL](#dumping-the-tls-certificate-using-openssl)
  - [TLS connection with a specific ciphersuite using OpenSSL](#tls-connection-with-a-specific-ciphersuite-using-openssl)
- [Windows](#windows)
  - [Shortcut to IE \(or WinINET\) Proxy Settings](#shortcut-to-ie-or-wininet-proxy-settings)
- [Amazon S3](#amazon-s3)
  - [Syncing a folder with an Amazon S3 bucket using s3cmd](#syncing-a-folder-with-an-amazon-s3-bucket-using-s3cmd)
  - [Changing the mime-type of CSS file after it is uploaded to avoid an old issue](#changing-the-mime-type-of-css-file-after-it-is-uploaded-to-avoid-an-old-issue)
- [Powershell](#powershell)
  - [List all files \(including hidden\)](#list-all-files-including-hidden)
  - [Diff in Powershell](#diff-in-powershell)
  - [Pseudo-grep in Powershell](#pseudo-grep-in-powershell)
  - [grep in command outputs](#grep-in-command-outputs)
  - [Get-Acl and icacls.exe](#get-acl-and-icaclsexe)
- [Some Git stuff because I keep forgetting them](#some-git-stuff-because-i-keep-forgetting-them)
  - [Create new branch and merge](#create-new-branch-and-merge)
  - [Only clone a certain branch](#only-clone-a-certain-branch)
  - [Undo remote git history after push](#undo-remote-git-history-after-push)
  - [Update local fork from original repo](#update-local-fork-from-original-repo)
- [Download Youtube videos with substitles](#download-youtube-videos-with-substitles)
- [Delete file or directory with a path or name over the Windows limit](#delete-file-or-directory-with-a-path-or-name-over-the-windows-limit)
- [Print Envelopes Using the Brother Printer and LibreOffice](#print-envelopes-using-the-brother-printer-and-libreoffice)

<!-- /MarkdownTOC -->

------
<a name="tar"></a>
## Tar
Insert xkcd, hur dur!

<a name="compressing-a-directory-using-tar"></a>
### Compressing a directory using tar
`tar -zcvf target_tar.tar.gz directory_to_be_compressed`

<a name="decompressing-a-targz-file"></a>
### Decompressing a tar.gz file
`tar -zxvf target_tar.tar.gz path/to/decompress/`

------

<a name="openssl"></a>
## OpenSSL

<a name="dumping-the-tls-certificate-using-openssl"></a>
### Dumping the TLS certificate using OpenSSL
`echo | openssl s_client -connect HOST:PORT 2>/dev/null | openssl x509 -text -noout`

<a name="tls-connection-with-a-specific-ciphersuite-using-openssl"></a>
### TLS connection with a specific ciphersuite using OpenSSL
`openssl s_client -connect HOST:PORT -cipher cipher-name -brief`

* `-brief`: reduced output
* `cipher-name`: A cipher from output of `openssl ciphers` command

------

<a name="windows"></a>
## Windows

<a name="shortcut-to-ie-or-wininet-proxy-settings"></a>
### Shortcut to IE (or WinINET) Proxy Settings

`control inetcpl.cpl,,4`

----------

<a name="amazon-s3"></a>
## Amazon S3

<a name="syncing-a-folder-with-an-amazon-s3-bucket-using-s3cmd"></a>
### Syncing a folder with an Amazon S3 bucket using s3cmd
`python s3cmd sync --acl-public --delete-removed --rr directory-to-sync/ s3://bucket-name`

For example uploading the Hugo public directory to my website:\\
`python s3cmd sync --acl-public --delete-removed --rr public/ s3://parsiya.net`

* `--acl-public`: Anyone can only read.
* `--delte-removed`: Delete objects with no corresponding local files.

<a name="changing-the-mime-type-of-css-file-after-it-is-uploaded-to-avoid-an-old-issue"></a>
### Changing the mime-type of CSS file after it is uploaded to avoid an old issue
`python s3cmd --acl-public --no-preserve --mime-type="text/css" put public/css/hugo-octopress.css s3://parsiya.net/css/hugo-octopress.css`

``` powershell
rd /q /s public
hugo
rd /q /s public\post
del /s /a .\*thumbs*.db
del /s /a public\categories\*index*.xml
del /s /a public\tags\*index*.xml
python s3cmd sync --acl-public --delete-removed -MP --no-preserve --rr public/ s3://parsiya.net
python s3cmd --acl-public --no-preserve --cf-invalidate --add-header="Expires: Sat, 20 Nov 2286 19:00:00 GMT"
       --mime-type="text/css" put public/css/hugo-octopress.css s3://parsiya.net/css/hugo-octopress.css
rd /q /s public
```

------

<a name="powershell"></a>
## Powershell

<a name="list-all-files-including-hidden"></a>
### List all files (including hidden)
`Get-ChildItem "searchterm" -recurse -force -path c:\ | select-object FullName`

* `-recurse`: recursive. Loops through all directories
* `-force`: list hidden files.
* `select-object`: Selects each file from last point
* `FullName`: Only display file name

<a name="diff-in-powershell"></a>
### Diff in Powershell
`Compare-Object (Get-Content new1.txt) (Get-Content new2.txt) | Format-List >> Diff-Output`

Output will be in format of

* `InputObject`: `c:\users\cigital\somefile` -- line content
* `SideIndicator`: `=>` -- exists in new2.txt (second file, file to the right)

<a name="pseudo-grep-in-powershell"></a>
### Pseudo-grep in Powershell
`findstr "something" *.txt`

will include filename and line (no number AFAIK)

`findstr /spin /c:"keyword" *.*`

* /s: recursive - will search through the current directory and all sub-directories
* /p: skip binary files (or files with characters that cannot be printed)
* /i: case-insensitive - remove if you want case sensitive search
* /n: print line number

If you want to search for different keywords (with OR) remove the `/c:`

`findstr /spin "keyword1 keyword2" *.*`

will search for keyword1 OR keyword2 in files

https://technet.microsoft.com/en-us/library/Cc732459.aspx

<a name="grep-in-command-outputs"></a>
### grep in command outputs
`whatever.exe | Select-String -pattern "admin"`

<a name="get-acl-and-icaclsexe"></a>
### Get-Acl and icacls.exe
`Get-Acl -path c:\windows\whatever.exe | Format-List`

`icacls.exe c:\windows\whatever.exe`

-----------

<a name="some-git-stuff-because-i-keep-forgetting-them"></a>
## Some Git stuff because I keep forgetting them

<a name="create-new-branch-and-merge"></a>
### Create new branch and merge
This works with small branches (e.g. one fix or so). Adapted from a [Bitbucket tutorial](https://confluence.atlassian.com/bitbucket/use-a-git-branch-to-merge-a-file-681902555.html).

1. Create new branch - `git branch fix-whatever`\\
This will create a branch of whatever branch you are currently on so make sure you are creating a branch from the branch you want.

2. Switch to the branch - `git checkout fix-whatever`

3. Make changes and commit - `git add - git commit`\\
Make any changes you want to do, then stage and commit.

4. Push the branch to remote repo [optional] - `git push`\\
This can be safely done because it's an obscure branch and no one else cares about it.

5. Go back to the original branch to merge - `git checkout master`\\
Master or whatever branch you were at step one.

6. Merge the branches - `git merge fix-whatever`.\\
Alternatively squash all commits into one `git merge --squash fix-whatever` and then `git commit -m "One message for all commits in merge"`.

7. Delete branch - `git branch -d fix-whatever`\\
We don't need it anymore. If it was pushed to remote, then we need to delete it there too.

<a name="only-clone-a-certain-branch"></a>
### Only clone a certain branch
`git clone -b <branch> <remote_repo>`

<a name="undo-remote-git-history-after-push"></a>
### Undo remote git history after push
Because this keeps happening to me.

1. Reset the head in local repo N commits back. - `git reset HEAD~N`\\
Where N is the number of commits that you want to revert.

2. Make changes and stage them - `git add`

3. Commit the changes - `git commit`

4. Force push the local repo to remote - `git push -f`\\
Note this will force the update and erase the commit history online. If not one else is using the repo in between it's ok.

<a name="update-local-fork-from-original-repo"></a>
### Update local fork from original repo

1. See current remotes - `git remote -v`

2. Make original repo the new remote upstream -\\
`git remote add upstream https://github.com/whatever/original-repo/`

3. Now we should see the new upstream with - `git remote -v`

4. Fetch upstream - `git fetch upstream`

5. Switch to your local master branch - `git checkout master`

6. Merge upstream/master into local master - `git merge upstream/master`

7. Push changes - `git push`

-----------

<a name="download-youtube-videos-with-substitles"></a>
## Download Youtube videos with substitles
I love Wuxia (Chinese martial arts if I am not mistaken) series and movies. The following [youtube-dl](https://github.com/rg3/youtube-dl/) command will download the 56 episode HQ quality Chinese TV series called `Xiao Ao Jiang Hu` or `Laughing in the Wind` (also called `The Smiling Proud Wanderer` or `Swordsman`).

`youtube-dl --ignore-errors --write-srt --sub-lang en --yes-playlist 'https://www.youtube.com/playlist?list=PLuGy72vdo4_ScwTYb1bAynhBs3KgowvvQ'`

```
--ignore-errors: continue after errors (in the case of a playlist we do not want to be interrupted for one error)
--write-srt    : download substitles
--sub-lang     : subtitle language (in this case English)
--yes-playlist : link to a Youtube playlist
```

`Youtube-dl` can be downloaded using `pip`. For example on Windows:\\
`python -m pip install youtube-dl`.

----------

<a name="delete-file-or-directory-with-a-path-or-name-over-the-windows-limit"></a>
## Delete file or directory with a path or name over the Windows limit

Answer from [superuser.com](http://superuser.com/a/467814).

``` posh
mkdir empty_dir
robocopy empty_dir the_dir_to_delete /s /mir
rmdir empty_dir
rmdir the_dir_to_delete
```

----------

<a name="print-envelopes-using-the-brother-printer-and-libreoffice"></a>
## Print Envelopes Using the Brother Printer and LibreOffice
Before printing, get to printer physically and use the following instructions:

* http://support.brother.com/g/b/faqend.aspx?c=gb&lang=en&prod=hl2170w_all&faqid=faq00000063_025

1. Open the back.
2. Press the two green handles down.
3. Open manual feed in front.
4. Adjust the paper guide and put the envelope in.
5. Put the envelope face up (the side that has the addresses should be up).
6. Insert it until the printer says `Please Wait` and grabs the paper.

Now open LibreOffice and use these instructions:

- https://www.pcmech.com/article/how-to-print-an-envelope-with-libreoffice/

1. Create new document in LibreOffice Writer (Word).
2. `Insert > Envelope`.
3. Enter destination in `Addressee`.
4. Check `Sender` and enter your own address in the bottom textbox.
5. Select `Printer` tab.
6. Select printer and press `Setup`.
7. Select the Brother printer and press `Properties`.
8. Select the following options:
    * Paper Size: `Com-10`.
    * Media Type: `Envelopes`.
    * Paper Source > First Page: `Manual`.
9. Print

<!-- links -->

[cheat-sheet-ext]: https://parsiya.net/cheatsheet
