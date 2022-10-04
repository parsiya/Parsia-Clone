---
draft: false
toc: true
comments: false
categories:
- Development
title: "CyberAces PowerShell Notes"
wip: false
snippet: "CyberAces 'Introduction to PowerShell' notes."
---

SANS has some free streaming tutorials. You can see them here:
https://tutorials.cyberaces.org/tutorials

This is pretty basic but I think the notes will act as a good summary that
people can read instead of watching the videos. These notes are now loosely
based on the videos and have a lot of items that I have added. If you follow the
videos and read the notes, the sequence of topics may not match.

## Case Sensitivity
I usually write the cmdlets in camel case but you usually do not have to. E.g.,
`man Get-ChildItem` and `man get-childitem` both work. Camel case helps with
readability.

## How to Get Help - This is Your Best Friend

* Before you start, open an admin PowerShell prompt and run `Update-Help`. In a
  normal prompt, not all modules can be updated. This may take a few minutes.
* After that you can essentially do `help command` or `help command -Examples`
  (the examples are great).
  * If the help page is longer than one screen you can do
    `help command -Examples | more` to paginate it.
* `Get-Help command -Full` shows everything so might want to paginate it all the
  time.

### Get-Help or help or man
Displays help. For example: `Get-Help ls` or `help ls` or `man ls`.

```powershell
PS C:\> get-help ls
NAME
    Get-ChildItem

SYNTAX
    Get-ChildItem [[-Path] <string[]>] [[-Filter] <string>] [-Include <string[]>] [-Exclude <string[]>] [-Recurse]
    [-Depth <uint32>] [-Force] [-Name] [-UseTransaction] [-Attributes <FlagsExpression[FileAttributes]> {ReadOnly |
    Hidden | System | Directory | Archive | Device | Normal | Temporary | SparseFile | ReparsePoint | Compressed |
    Offline | NotContentIndexed | Encrypted | IntegrityStream | NoScrubData}] [-Directory] [-File] [-Hidden]
    [-ReadOnly] [-System]  [<CommonParameters>]

    Get-ChildItem [[-Filter] <string>] -LiteralPath <string[]> [-Include <string[]>] [-Exclude <string[]>] [-Recurse]
    [-Depth <uint32>] [-Force] [-Name] [-UseTransaction] [-Attributes <FlagsExpression[FileAttributes]> {ReadOnly |
    Hidden | System | Directory | Archive | Device | Normal | Temporary | SparseFile | ReparsePoint | Compressed |
    Offline | NotContentIndexed | Encrypted | IntegrityStream | NoScrubData}] [-Directory] [-File] [-Hidden]
    [-ReadOnly] [-System]  [<CommonParameters>]

ALIASES
    gci
    ls
    dir

REMARKS
    Get-Help cannot find the Help files for this cmdlet on this computer. It is displaying only partial help.
        -- To download and install Help files for the module that includes this cmdlet, use Update-Help.
        -- To view the Help topic for this cmdlet online, type: "Get-Help Get-ChildItem -Online" or
           go to http://go.microsoft.com/fwlink/?LinkID=113308.
```

* In order to `Update-Help` run in it an admin PowerShell window. Otherwise, it
  cannot update all modules. It takes a while to update everything.
* By default it does not show all the help. We can use `-Full` or `-Examples` to
  show more. Warning `-Full` returns a ton of stuff.

```powershell
PS> get-help ls -examples
NAME
    Get-ChildItem

SYNOPSIS
    Gets the items and child items in one or more specified locations.

    Example 1: Get child items in the current directory

    PS C:\>Get-ChildItem

    This command gets the child items in the current location. If the location is a file system directory, it gets the
    files and sub-directories in the current directory. If the item does not have child items, this command returns to
    the command prompt without displaying anything.
```
* You can filter by Noun. For example `Get-Command -Noun Service`:

```powershell
PS C:\> Get-Command -Noun service

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Cmdlet          Get-Service                                        3.1.0.0    Microsoft.PowerShell.Management
Cmdlet          New-Service                                        3.1.0.0    Microsoft.PowerShell.Management
Cmdlet          Restart-Service                                    3.1.0.0    Microsoft.PowerShell.Management
Cmdlet          Resume-Service                                     3.1.0.0    Microsoft.PowerShell.Management
Cmdlet          Set-Service                                        3.1.0.0    Microsoft.PowerShell.Management
Cmdlet          Start-Service                                      3.1.0.0    Microsoft.PowerShell.Management
Cmdlet          Stop-Service                                       3.1.0.0    Microsoft.PowerShell.Management
Cmdlet          Suspend-Service                                    3.1.0.0    Microsoft.PowerShell.Management
```

* Or filter by Module. Useful for 3rd party modules. E.g.,
  `Get-Command -Module Microsoft.PowerShell.Core`:

```powershell
PS C:\> Get-Command -Module Microsoft.PowerShell.Core

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Cmdlet          Add-History                                        3.0.0.0    Microsoft.PowerShell.Core
Cmdlet          Add-PSSnapin                                       3.0.0.0    Microsoft.PowerShell.Core
Cmdlet          Clear-History                                      3.0.0.0    Microsoft.PowerShell.Core
Cmdlet          Connect-PSSession                                  3.0.0.0    Microsoft.PowerShell.Core
Cmdlet          Debug-Job                                          3.0.0.0    Microsoft.PowerShell.Core
Cmdlet          Disable-PSRemoting                                 3.0.0.0    Microsoft.PowerShell.Core
```

* It also has this search feature. If you do not know what exactly you are
  looking for, just do `man whatever` and it will find you the cmdlets that have
  `whatever` in them:

```powershell
PS C:\> man executionpolicy

Name                              Category  Module                    Synopsis
----                              --------  ------                    --------
Get-ExecutionPolicy               Cmdlet    Microsoft.PowerShell.S... Gets the execution policies for the current se...
Set-ExecutionPolicy               Cmdlet    Microsoft.PowerShell.S... Changes the user preference for the Windows Po...
```

## Aliases
Some commands have aliases.

* For example `dir` or `ls` both work because they are aliases of `Get-ChildItem`.
* You can create, delete and modify aliases.

### Get-Alias Cmdlet
* https://technet.microsoft.com/en-us/library/ee176839.aspx
* To see all aliases use the `Get-Alias` command.
* To see aliases for a certain command use `Get-Alias -name l*` which shows all
  aliases which start with `l`.

```powershell
PS> Get-Alias l*
CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           lp -> Out-Printer
Alias           ls -> Get-ChildItem
```

* Or just search what an alias points to like `Get-Alias dir`:

```powershell
PS> Get-Alias dir
CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           dir -> Get-ChildItem
```

* To search the aliases for a cmdlet use `Get-Alias -Definition Get-ChildItem`:

```powershell
PS>Get-Alias -Definition get-childitem
CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           dir -> Get-ChildItem
Alias           gci -> Get-ChildItem
Alias           ls -> Get-ChildItem
```

### Set-Alias
To create our own alias use `Set-Alias -Name mydir -Value ls`:

```powershell
PS> Set-Alias -Name mydir -Value ls
PS> Get-Alias -Definition ls

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           mydir -> Get-ChildItem
```

Note that this is an alias for `ls` so it does not show up in the list of
aliases for `Get-ChildItem` (which `ls` is an alias of):

```powershell
PS C:\> Get-Alias -Definition Get-ChildItem

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           dir -> Get-ChildItem
Alias           gci -> Get-ChildItem
Alias           ls -> Get-ChildItem
```

### Common Aliases Between PowerShell and Bash
A lot of PowerShell aliases are the name of bash commands. For example `man` is
and alias for `help`:

```powershell
PS C:\> Get-Alias -Definition Help

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           man -> help
```

A couple of cheat sheets:

* http://xahlee.info/powershell/PowerShell_for_unixer.html
* http://cecs.wright.edu/~pmateti/Courses/233/Labs/Scripting/bashVsPowerShellTable.html
* http://cecs.wright.edu/~pmateti/Courses/233/Top/233-CheatSheet.html

-------------

## Session 1 - Introduction to PowerShell
https://tutorials.cyberaces.org/tutorials/view/3-3-1

### Naming Convention
`Verb-Noun`. Things like `Get-Service`.

### Parameters
Can be positional or named. Personally I prefer named because it's more readable.

* You can shorten parameter names to the extent that they are still unique.

```powershell
Get-ChildItem -Filter *.exe
Get-ChildItem -Filt *.exe
Get-ChildItem -Fi *.exe
```

* `-F` will not work because `Get-ChildItem` has a `-Force` option.

### Get-Member
In PowerShell everything is an object. We can use `Get-Member` to get properties
and methods of object(s).

```powershell
PS C:\> Get-ChildItem | Get-Member
   TypeName: System.IO.DirectoryInfo
Name                      MemberType     Definition
----                      ----------     ----------
LinkType                  CodeProperty   System.String LinkType{get=GetLinkType;}
Mode                      CodeProperty   System.String Mode{get=Mode;}
Target                    CodeProperty   System.Collections.Generic.IEnumerable`1[[System.String, mscorlib, Version=...
Create                    Method         void Create(), void Create(System.Security.AccessControl.DirectorySecurity ...
```

Also works for aliases like `ls | Get-Member`.

### Piping
We can pipe outputs of one command to the other. In PowerShell everything is an
object and not text like bash (take that plebs lol).

For example we can see the output of the previous command is truncated. In order
to format it properly we can use `Format` cmdlets.

A good [tutorial][piping-tutorial]. Usually I just use `Format-List` to prevent
truncation. It shows data in a list.

```powershell
PS> Get-ChildItem | Get-Member | Format-List
TypeName   : System.IO.DirectoryInfo
Name       : LinkType
MemberType : CodeProperty
Definition : System.String LinkType{get=GetLinkType;}

TypeName   : System.IO.DirectoryInfo
Name       : Mode
MemberType : CodeProperty
Definition : System.String Mode{get=Mode;}

TypeName   : System.IO.DirectoryInfo
Name       : Target
MemberType : CodeProperty
Definition : System.Collections.Generic.IEnumerable`1[[System.String, mscorlib, Version=4.0.0.0, Culture=neutral,
             PublicKeyToken=b77a5c561934e089]] Target{get=GetTarget;}
```

<!-- Section 1 links -->
[piping-tutorial]:https://msdn.microsoft.com/en-us/powershell/scripting/getting-started/cookbooks/using-format-commands-to-change-output-view

---------------------

## Session 2 - Cmdlets
https://tutorials.cyberaces.org/tutorials/view/3-3-2

### Get-ChildItem
This is a good cmdlet. Aliases are `dir`, `ls` and `gci`.

* Run `man Get-ChildItem -Examples` for examples.

#### Read Registry
* Read a registry hive `ls HKCU:`
* To get a specific registry key `Get-ChildItem -Path "HKLM:\Software"`.

```powershell
PS> ls HKCU:

    Hive: HKEY_CURRENT_USER

Name                           Property
----                           --------
AppEvents
AppXBackupContentType
Console                        ColorTable00             : 0
                               ColorTable01             : 8388608
                               ColorTable02             : 32768
                               ColorTable03             : 8421376
                               ColorTable04             : 128
                               ColorTable05             : 8388736
```

#### Read Windows Certificate Store
* Read the Windows certificate store `ls cert:`
* https://technet.microsoft.com/en-us/library/hh847761.aspx
* `cert:` is essentially a new drive similar to `HKCU:`


* `ls cert:` lists machine's certificate stores:

```powershell
PS> ls cert:

Location   : CurrentUser
StoreNames : {TrustedPublisher, ClientAuthIssuer, Root, UserDS...}

Location   : LocalMachine
StoreNames : {TrustedPublisher, ClientAuthIssuer, Remote Desktop, Root...}
```

* Now we can see what's inside the `LocalMachine` certificate store with `ls cert:LocalMachine`:

```powershell
PS C:\> ls cert:LocalMachine

Name : TrustedPublisher
Name : ClientAuthIssuer
Name : Remote Desktop
Name : Root
Name : TrustedDevices
Name : CA
Name : Windows Live ID Token Issuer
```

* We can go deeper (note that we can use double quotes with paths with space):

```powershell
PS> ls "cert:LocalMachine\Windows Live ID Token Issuer" | Format-List

Subject      : CN=Token Signing Public Key
Issuer       : CN=Token Signing Public Key
Thumbprint   : 2C85006A1A028BCC349DF23C474724C055FDE8B6
FriendlyName :
NotBefore    : 5/9/2016 4:40:55 PM
NotAfter     : 5/8/2021 4:40:55 PM
Extensions   : {System.Security.Cryptography.Oid, System.Security.Cryptography.Oid, System.Security.Cryptography.Oid,
               System.Security.Cryptography.Oid}

Subject      : CN=Token Signing Public Key
Issuer       : CN=Token Signing Public Key
Thumbprint   : 0217922CA1B6F0BD0F1D7FF6E7BDC29B2FAAA060
FriendlyName :
NotBefore    : 7/2/2013 5:10:37 PM
NotAfter     : 7/1/2018 5:10:37 PM
Extensions   : {System.Security.Cryptography.Oid, System.Security.Cryptography.Oid, System.Security.Cryptography.Oid,
               System.Security.Cryptography.Oid}

PS> ls "cert:LocalMachine\CA" | Format-List

Subject      : CN=Root Agency
Issuer       : CN=Root Agency
Thumbprint   : FEE449EE0E3965A5246F000E87FDE2A065FD89D4
FriendlyName :
NotBefore    : 5/28/1996 6:02:59 PM
NotAfter     : 12/31/2039 6:59:59 PM
Extensions   : {System.Security.Cryptography.Oid, System.Security.Cryptography.Oid}

Subject      : OU=www.verisign.com/CPS Incorp.by Ref. LIABILITY LTD.(c)97 VeriSign, OU=VeriSign International Server
               CA - Class 3, OU="VeriSign, Inc.", O=VeriSign Trust Network
Issuer       : OU=Class 3 Public Primary Certification Authority, O="VeriSign, Inc.", C=US
Thumbprint   : D559A586669B08F46A30A133F8A9ED3D038E2EA8
FriendlyName :
NotBefore    : 4/16/1997 8:00:00 PM
NotAfter     : 10/24/2016 7:59:59 PM
Extensions   : {System.Security.Cryptography.Oid, System.Security.Cryptography.Oid, System.Security.Cryptography.Oid,
               System.Security.Cryptography.Oid...}
```

* Even deeper and see certificate info based on thumbprint:

```powershell
PS C:\> ls "cert:LocalMachine\CA\D559A586669B08F46A30A133F8A9ED3D038E2EA8" | Format-List -Property *


PSPath                   : Microsoft.PowerShell.Security\Certificate::LocalMachine\CA\D559A586669B08F46A30A133F8A9ED3D0
                           38E2EA8
PSParentPath             : Microsoft.PowerShell.Security\Certificate::LocalMachine\CA
PSChildName              : D559A586669B08F46A30A133F8A9ED3D038E2EA8
PSDrive                  : Cert
PSProvider               : Microsoft.PowerShell.Security\Certificate
PSIsContainer            : False
EnhancedKeyUsageList     : {Server Authentication (1.3.6.1.5.5.7.3.1), Client Authentication (1.3.6.1.5.5.7.3.2),
                           2.16.840.1.113730.4.1, 2.16.840.1.113733.1.8.1}
DnsNameList              :
SendAsTrustedIssuer      : False
EnrollmentPolicyEndPoint : Microsoft.CertificateServices.Commands.EnrollmentEndPointProperty
EnrollmentServerEndPoint : Microsoft.CertificateServices.Commands.EnrollmentEndPointProperty
PolicyId                 :
Archived                 : False
Extensions               : {System.Security.Cryptography.Oid, System.Security.Cryptography.Oid,
                           System.Security.Cryptography.Oid, System.Security.Cryptography.Oid...}
FriendlyName             :
IssuerName               : System.Security.Cryptography.X509Certificates.X500DistinguishedName
NotAfter                 : 10/24/2016 7:59:59 PM
NotBefore                : 4/16/1997 8:00:00 PM
HasPrivateKey            : False
PrivateKey               :
PublicKey                : System.Security.Cryptography.X509Certificates.PublicKey
RawData                  : {48, 130, 3, 131...}
SerialNumber             : 46FCEBBAB4D02F0F926098233F93078F
SubjectName              : System.Security.Cryptography.X509Certificates.X500DistinguishedName
SignatureAlgorithm       : System.Security.Cryptography.Oid
Thumbprint               : D559A586669B08F46A30A133F8A9ED3D038E2EA8
Version                  : 3
Handle                   : 2694988070352
Issuer                   : OU=Class 3 Public Primary Certification Authority, O="VeriSign, Inc.", C=US
Subject                  : OU=www.verisign.com/CPS Incorp.by Ref. LIABILITY LTD.(c)97 VeriSign, OU=VeriSign
                           International Server CA - Class 3, OU="VeriSign, Inc.", O=VeriSign Trust Network
```

### cd or Change Directory
It's easier to treat registry and the certificate store as drives and cd into
them.

```powershell
PS C:\> cd cert:
PS Cert:\> dir

Location   : CurrentUser
StoreNames : {TrustedPublisher, ClientAuthIssuer, Root, UserDS...}

Location   : LocalMachine
StoreNames : {TrustedPublisher, ClientAuthIssuer, Remote Desktop, Root...}


PS Cert:\> cd .\\CurrentUser\
PS Cert:\CurrentUser\> dir

Name : TrustedPublisher
Name : ClientAuthIssuer
Name : Root
Name : UserDS
Name : CA
Name : ACRS
```

-----------------------

## Session 3: Scripting, Variables and Syntax
https://tutorials.cyberaces.org/tutorials/view/3-3-3

Scripts are in `ps1` files. They do not run with double-click.

### ExecutionPolicy
In order to run them we need to change the execution policy. Default setting
doesn't run scripts.

* You can view computer's execution policies with `Get-ExecutionPolicy -List`:

```powershell
PS C:\> Get-ExecutionPolicy -List

        Scope ExecutionPolicy
        ----- ---------------
MachinePolicy       Undefined
   UserPolicy       Undefined
      Process       Undefined
  CurrentUser       Undefined
 LocalMachine    RemoteSigned
```

* `Set-ExecutionPolicy` sets a policy (needs admin powershell window). There are
  four options ([technet source][executionpolicy-technet]):
    * Restricted - No scripts can be run. Windows PowerShell can be used only in
      interactive mode.
    * AllSigned - Only scripts signed by a trusted publisher can be run.
    * RemoteSigned - Downloaded scripts must be signed by a trusted publisher
      before they can be run.
    * Unrestricted - No restrictions; all Windows PowerShell scripts can be run.

### Variables
* Prefixed with `$`.
* Set variable: `$a = 13`.
* Get variable: `$a`.
* Store the result of a command into a variable: `$output = dir cert:`.

#### Variable Types
Create a typed variable: `[int]$thisIsAnInt = 11`.

These are the different types ([source technet][variabletypes-technet]):

* [int] 32-bit signed integer
* [long] 64-bit signed integer
* [string] Fixed-length string of Unicode characters
* [char] Unicode 16-bit character
* [bool] True/false value
* [byte] 8-bit unsigned integer
* [double] Double-precision 64-bit floating point number
* [decimal] 128-bit decimal value
* [single] Single-precision 32-bit floating point number
* [array] Array of values
* [xml] Xmldocument object
* [hashtable] Hashtable object (similar to a Dictionary object)

### Arrays
Collection of objects. Use them like normal arrays in programming languages.

* Help on Technet: https://technet.microsoft.com/en-us/library/hh847882.aspx

```powershell
# Create an array
PS C:\> $someNumbers = 0, 1, 2, 3, 4

# Access all of it - echo $someNumbers does the same thing
PS C:\> $someNumbers
0
1
2
3
4

# Access a specific index - indexing starts from 0 like almost every programming language
PS C:\> $someNumbers[3]
3

# Negative indexing also works
# -1 is the last item
PS C:\> $someNumbers[-1]
4

# -2 works as intended
PS C:\> $someNumbers[-2]
3

# Get length of array - either use Length or Count properties
PS C:\> $someNumbers.Count
5
PS C:\> $someNumbers.Length
5

# But remember that they are ReadOnly
PS C:\> $someNumbers.Count = 10
'Count' is a ReadOnly property.
At line:1 char:1
+ $someNumbers.Count = 10
+ ~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertyAssignmentException

# Get the type - this is because our array was not typed when we created it
# As a result the members can be of different types
PS C:\> $someNumbers.GetType()
IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     True     Object[]                                 System.Array

# Create a typed array - note inside the brackets
# Type of a typed array is something like int[] or int32[]
PS C:\> [int[]]$intArray = 0, 1, 2, 3

# Now we can see the correct type
PS C:\> $intArray.GetType()
IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     True     Int32[]                                  System.Array

# Type can be any .NET framework object
PS C:\> [Diagnostics.Process[]]$processes = Get-Process

PS C:\> $processes

Handles  NPM(K)    PM(K)      WS(K) VM(M)   CPU(s)     Id  SI ProcessName
-------  ------    -----      ----- -----   ------     --  -- -----------
    247      21    28388      54672   220    60.14   2472   2 atom
    244      23    22656      34136   288    40.33   4908   2 atom
    171      15     4364      10528   156     0.34   6800   2 atom
    547      37    52600      80496   332    55.59   8104   2 atom
    347      67   626812     647076  1006   361.66   8848   2 atom

# You can use ranges
# Here powershell doesn't care if your range is over the bounds, it just shows all of the array
PS C:\> $someNumbers[0..10]
0
1
2
3
4

# You can use negative index in range - you can see it is reading backwards
PS C:\> $someNumbers[0..-3]
0
4
3
2

# Or use the range like this to view specific members
PS C:\> $someNumbers[0,2,4]
0
2
4

# Combine a range and specific indices with +
# Seems like when you use the + it cannot be used for the first item (otherwise the parser thinks it's a mathematical operation to calculate an index)
# You can do this
PS C:\> $someNumbers[2,0+1..3]
2
0
1
2
3

# But cannot do this
PS C:\> $someNumbers[2+1..3]
Method invocation failed because [System.Object[]] does not contain a method named 'op_Addition'.
At line:1 char:1
+ $someNumbers[2+1..3]
+ ~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (op_Addition:String) [], RuntimeException
    + FullyQualifiedErrorId : MethodNotFound

# To add items to arrays use += (obviously respect the type of the array)
PS C:\> $someNumbers
0
1
2
3
4

PS C:\> $someNumbers += 5

PS C:\> $someNumbers
0
1
2
3
4
5

# Combine arrays with +
PS C:\> $moreNumbers = 10,11,12,13

PS C:\> $combined = $someNumbers + $moreNumbers

PS C:\> $combined
0
1
2
3
4
5
10
11
12
13

# To delete an array set it to $null
PS C:\> $combined = $null
PS C:\> $combined
PS C:\> $combined.Count
0
```

### Get-Member
To get methods and properties of an object, pipe it to `Get-Member`.

```powershell
# Like an int
PS C:\> 1 | Get-Member
   TypeName: System.Int32

Name        MemberType Definition
----        ---------- ----------
CompareTo   Method     int CompareTo(System.Object value), int CompareTo(int value), int IComparab...
Equals      Method     bool Equals(System.Object obj), bool Equals(int obj), bool IEquatable[int]....
GetHashCode Method     int GetHashCode()
GetType     Method     type GetType()
...

# Same thing can be done with an array
PS C:\> [int[]]$intArray = 10, 9, 8, 7, 6

PS C:\> $intArray.GetType()
IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     True     Int32[]                                  System.Array

PS C:\> $intArray | Get-Member
   TypeName: System.Int32

Name        MemberType Definition
----        ---------- ----------
CompareTo   Method     int CompareTo(System.Object value), int CompareTo(int value), int IComparab...
Equals      Method     bool Equals(System.Object obj), bool Equals(int obj), bool IEquatable[int]....
GetHashCode Method     int GetHashCode()
GetType     Method     type GetType()

# If we want to see the type of members in an array
# $arrayName | Get-Member
# will send members of the array one by one
```

#### Get-ChildItem variable:
Returns all available variables.

```powershell
PS C:\> Get-ChildItem variable:

Name                           Value
----                           -----
$                              clear
?                              True
^                              clear
args                           {}
mixedArray                     {1, hello, 2.3}
moreNumbers                    {10, 11, 12, 13}
someNumbers                    {0, 1, 2, 3...}
```

### User Properties of Cmdlet Output
Cmdlets do not have properties by themselves, their output is an object which
has properties.

E.g., the output of `Get-Process` is an array with members of type
`System.Diagnostics.Process`. We can get the first member and see its methods:

```powershell
PS C:\> (Get-Process)[0] | Get-Member
   TypeName: System.Diagnostics.Process

Name                       MemberType     Definition
----                       ----------     ----------
Handles                    AliasProperty  Handles = Handlecount
Name                       AliasProperty  Name = ProcessName
...

# Executing one of the methods is also simple
PS C:\> (Get-Process)[30].ToString()
System.Diagnostics.Process (chrome)

# Or read a Property
PS C:\> (Get-Process)[30].ProcessName
chrome
```

### Double Quotes vs. Single Quotes
Double quote expands the value inside while single quote doesn't.

```powershell
PS C:\> echo "This is the array $someNumbers"
This is the array 0 1 2 3 4 5

PS C:\> echo 'This is the array $someNumbers'
This is the array $someNumbers
```

You can escape stuff in double quotes to prevent them from being expanded with
backtick (cannot do it here because it will mess with markdown highlighting):

```powershell
PS C:\> echo "This is the array `$somenumbers`: $someNumbers"
This is the array $somenumbers: 0 1 2 3 4 5
```

To expand properties of objects, wrap them in `()`. Otherwise, it will just print
the variable and then put the text of the method after it:

```powershell
PS C:\> echo "Today is $(Get-Date)"
Today is 07/29/2016 17:49:01

PS C:\> echo "Today is $((Get-Date).DayOfWeek)"
Today is Friday

PS C:\> echo "Today is $(Get-Date).DayOfWeek"
Today is 07/29/2016 17:49:22.DayOfWeek
```

<!-- Section 3 links -->
[executionpolicy-technet]: https://technet.microsoft.com/en-us/library/ee176961.aspx
[variabletypes-technet]: https://technet.microsoft.com/en-us/magazine/ff642464.aspx

----------------------

## Section 4 - Flow Control
https://tutorials.cyberaces.org/tutorials/view/3-3-4

### WhatIf - Confirm - Verbose
These are three switches that help with running commands. `WhatIf` is the most
interesting (and probably useful).

* **-WhatIf** does not run the command. Instead it says what it would do if it was executed.
* **-Confirm** does what it says. It asks for confirmation before running the command.
* **-Verbose** runs the command but gives us extra information.

For example let's try to create a directory with `mkdir` (which is not exactly
an alias for `New-Item` although if you run `help mkdir` we will see info for
`New-Item`):

```powershell
# Testing -WhatIf
PS C:\test> mkdir new-directory -WhatIf
What if: Performing the operation "Create Directory" on target "Destination: C:\test\new-directory".

# But the command was not actually executed because ls returns nothing
PS C:\test> ls
PS C:\test>

# Testing -Confirm
PS C:\test> mkdir new-directory -Confirm

Confirm
Are you sure you want to perform this action?
Performing the operation "Create Directory" on target "Destination: C:\test\new-directory".
[Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "Y"): L
PS C:\test>

# Testing -Verbose
# It actually runs the command but gives us extra info.
PS C:\test> mkdir new-directory -Verbose
VERBOSE: Performing the operation "Create Directory" on target "Destination: C:\test\new-directory".

    Directory: C:\test

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        7/31/2016   7:18 PM                new-directory
```

Not all commands have these. Usually PowerShell core commands that
**change the state of the machine** have this. E.g., `ls` does not have neither
`-Confirm` nor `-WhatIf` and `-Verbose` does not change its behavior.

To see what commands support `-WhatIF` we can run the following PowerShell
command [source at computerperformance.co.uk][source-computerperformance]
(similar for `-Confirm` and `-Verbose`):

```powershell
Get-Command -commandType cmdlet | where { $_.parameters.keys -Contains "Confirm"} | Format-Table Name
```

We can add support for these commands to our own scripts as shown here:  
https://blogs.msdn.microsoft.com/powershell/2007/02/25/supporting-whatif-confirm-verbose-in-scripts/

### Operators

* Operators are at: https://technet.microsoft.com/en-us/library/hh847732.aspx.

| Operator | Meaning |
| :------------- | :------------- |
| -eq | Equal |
| -ne |	Not equal |
| -lt	| Less than |
| -le	| Less than or equal |
| -gt | Greater than |
| -ge |	Greater than or equal |
| -match | regex match |
| -notmatch | negative regex match |
| -like | wildcard match |
| -notlike | negative wildcard match |
| -and | && |
| -or | or |
| -xor | XOR |
| -not | not |
| % | mod |

### If - Then - Else
Usage is similar to programming languages (there is no `then` either).

To create these scripts, it's easier to just use the `PowerShell_ise.exe`
(PowerShell Integrated Scripting Environment).

Create a new script and write it on top. Run the script using the button or
press `F5` and the bottom panel will show the result.

```powershell
PS C:\> $ten = 10
if ($ten -eq 0)
    { "Ten does not equal zero." }
elseif ($ten -lt 5)
    { "Ten is not less than 5." }
else
    { "Ten is ten." }

Ten is ten.
```

### Where-Object Filtering
Has two aliases

```powershell
PS C:\> get-Alias -Definition where-object

CommandType     Name
-----------     ----
Alias           ? -> Where-Object
Alias           where -> Where-Object
```

Pipe the output of a command to `Where-Object` (or one of the aliases). Then
inside the block you can use `$_` to refer to it. Imagine it's like a for that
goes through each member of the output and you can filter. To take action (as in
run a new command use `ForEach-Object`).

```powershell
PS C:\Python27> ls | ? {$_.Name -like "*py*"}
    Directory: C:\Python27
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        12/5/2015   8:41 PM          28160 python.exe
-a----        12/5/2015   8:41 PM          28160 pythonw.exe

# We can use different format (perhaps more readable) too (this will work for all three)
PS C:\Python27> ls | Where Name -Like "*py*"
    Directory: C:\Python27
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        12/5/2015   8:41 PM          28160 python.exe
-a----        12/5/2015   8:41 PM          28160 pythonw.exe

# We can practice a little regex with -Match
PS C:\Python27> ls | ? Name -Match ".*py"
    Directory: C:\Python27
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        12/5/2015   8:41 PM          28160 python.exe
-a----        12/5/2015   8:41 PM          28160 pythonw.exe
```

### ForEach-Object
Similar to `Where-Object` but you can run a new command with each iterated item.

* https://technet.microsoft.com/en-us/library/ee176828.aspx

```powershell
PS C:\>Get-Process | % { Write $($_.ProcessName + "-" + $_.Id) }
```

To concat two strings for printing like above do `$( $_.whatever + "something" )`.

```powershell
# Rename jpeg files to jpeg
ls *.jpeg |  ren -NewName {$_.BaseName +".jpg"}
```

### Select-Object
"Filter properties so only certain ones are passed through the pipeline."

We can recreate the `$_.ProcessName` command because items passed through end of
last pipe are printed on the screen.

```powershell
PS C:\> Get-Process | Select-Object ProcessName, Id
```

**But how do we process the tuple in the next pipe line (e.g. Write)? do we do $_[0]? Is the output an array?**

### Output and the Format Verb
We can format output. We have seen them before.

* `Format-Table` or `ft`.
* `Format-List` or `fl`.

```powershell
PS C:\>Get-Process | ft
PS C:\>Get-Process | fl

# Without parameters they only display the default fields, use * to display all
PS C:\>Get-Process | ft *
PS C:\>Get-Process | fl *

# The Autosize parameter adjusts the column widths to minimize truncation.
PS C:\>Get-Process | ft -Auto

# You can do Groupbys
PS C:\> Get-Process | ft -GroupBy ProcessName
   ProcessName: atom

Handles  NPM(K)    PM(K)      WS(K) VM(M)   CPU(s)     Id  SI ProcessName
-------  ------    -----      ----- -----   ------     --  -- -----------
    274      22    26852      39156   226    23.77   1136   5 atom
    546      36    51260      77708   332    11.77   6584   5 atom
    245      23    20852      32160   289     9.08   7524   5 atom
    346      47   294676     308828   665    65.30   7644   5 atom
    175      15     4508      10880   156     0.36   8420   5 atom

# Usually it's a good idea to sort the output based on the GroupBy in the table before piping it to the table
PS C:\> Get-Process | Sort-Object ProcessName | Format-Table -GroupBy ProcessName
```

### File Output
Using the redirection `>` it only uses Unicode. Instead we can use `Out-File` to
get ASCII etc. `Out-File` also has more options.

```powershell
# Write to a file
PS C:\test> Get-Process | Out-File process1.txt
PS C:\test> ls
    Directory: C:\test
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         8/1/2016   4:19 PM          30506 process1.txt

# By default Out-File will overwrite any existing files.
# -Append does what it says
PS C:\test> Get-Process | Out-File process1.txt -Append
PS C:\test> ls
    Directory: C:\test
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         8/1/2016   4:22 PM          61494 process1.txt

# -NoClobber will prevent over-writing, PowerShell will give you an error if the file already exists
PS C:\test> Get-Process | Out-File process1.txt -NoClobber
Out-File : The file 'C:\test\process1.txt' already exists.
At line:1 char:15
+ Get-Process | Out-File process1.txt -NoClobber
+               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ResourceExists: (C:\test\process1.txt:String) [Out-File], IOException
    + FullyQualifiedErrorId : NoClobber,Microsoft.PowerShell.Commands.OutFileCommand
```

Send output in ASCII format (by default it is Unicode).

```powershell
PS C:\test> Get-Process | Out-File process1.txt -Encoding ASCII
```
You can also use the redirection `>`.

* `>`: Overwrite
* `>>`: Append


* `1>`: Same as `>`
* `2>`: Redirect errors
* `3>`: Redirect warnings
* `4>`: Debug

Combinations work too: `2>&1`.

### Export-CSV and Import-CSV
We can export the files in CSV format. It will create the columns too. Then we
can open these CSV files in Excel.

Later we can import them back into variables (for example).

```powershell
# Export running processes (and their other info) to a csv file
PS C:\test> Get-Process | Export-CSV process1.csv

# Now importing back from file
PS C:\test> $processes = Import-CSV process1.csv

# Display the variable in the table format
PS C:\test> $processes | Format-Table

Name                     SI Handles VM            WS        PM        NPM    Path
----                     -- ------- --            --        --        ---    ----
alg                      0  89      2199052992512 2244608   1642496   8480
AMPAgent                 0  205     80158720      11603968  3735552   19048
```

We can `Import-CSV` without the header and choosing the delimiter

```powershell
$csvfile = Import-CSV -Delimiter " " -Path whatever.txt -Header "Column1", "Column2", "Column3"

# Now we can do stuff for columns, like sort by a column.
$csvfile | sort -Property Column3 -Descending

# or do math stuff
$csvfile | Measure-Object -Property Column3 -Ave -Min -Max
```

### Measure-Object
"Calculates numeric properties of objects."

```powershell
# Calculate the number of files and directories
PS C:\test> ls | Measure-Object
Count    : 2
Average  :
Sum      :
Maximum  :
Minimum  :
Property :

PS C:\test> ls
    Directory: C:\test
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         8/1/2016   5:07 PM          82290 process1.csv
-a----         8/1/2016   4:22 PM          61494 process1.txt

# Do stuff with file length
PS C:\test> Get-ChildItem | Measure-Object -Property length -Minimum -Maximum -Average
Count    : 2
Average  : 71892
Sum      :
Maximum  : 82290
Minimum  : 61494
Property : Length

# Measure characters, words and lines in a text file
PS C:\test> cat .\process1.txt | Measure-Object -Word -Line -Character

Lines Words Characters Property
----- ----- ---------- --------
  254  2160      30226
```

## Section 5 - Practical Uses & Conclusion
https://tutorials.cyberaces.org/tutorials/view/3-3-5

### Ping All IPs in a Range
`PS C:\> 1..254 | % { ping "192.168.0.$_" }`

### Process Manipulation
Things to do with processes.

```powershell
# Start a process
PS C:\> Start-Process -FilePath "notepad.exe"
PS C:\> Start-Process notepad

# We get more control with Start-Process

# Redirect input and output
# From Get-Help Start-Process -Examples
PS C:\> Start-Process -FilePath "Sort.exe" -RedirectStandardInput "Testsort.txt" -RedirectStandardOutput
    "Sorted.txt" -RedirectStandardError "SortError.txt" -UseNewEnvironment
# The UseNewEnvironment parameter specifies that the process runs with its own environment variables.

# Start a process in a maximized window
PS C:\> Start-Process -FilePath "notepad" -Wait -WindowStyle Maximized

# Start Windows PowerShell as an administrator
PS C:\> Start-Process -FilePath "powershell" -Verb runAs

#  Starts a PowerShell process in a new console window.
PS C:\> Start-Process -FilePath "powershell.exe" -Verb open
```

Kill process by ID, name or path

```powershell
# PID
Stop-Process 1234

# Name
Stop-Process notepad

# Path
ps | ? { $_.Path -Like "C:\python27\*" } | kill
```
### -Verb
What are these verbs? The verbs are determined by the file extension.

To find Verbs for each file use:

```powershell
PS C:\test> $txtFile = New-Object System.Diagnostics.ProcessStartInfo -Args process1.txt
PS C:\test> $txtFile.Verbs
open
print
printto

# Now we can run one the verbs
# This will open it in notepad (default program for txt files)
PS C:\test> Start-Process -FilePath .\process1.txt -Verb open

# We can print it with the Print Verb
```

### Iterate Through Files in a Folder
Folders (directories) are containers while files are not. We can check it with
`PsIsContainer`.

```powershell
ls | ? { !$_.PsIsContainer } == ls | ? { -not $_.PsIsContainer }

# To view hidden and system files
# -Fo or -Force
ls -Force
```

### Get-FileHash
Calculate file hash using different hashing algorithms. PowerShell 4.0 and up.

```powershell
# Default algorithm is SHA256 and as you can see the output is truncated (because it's too long).
PS C:\test> Get-FileHash .\process1.txt

Algorithm       Hash                                                                   Path
---------       ----                                                                   ----
SHA256          FDA966B28DB48262D48DBC1680268B5DE814F0D3E2BBFEC4F7C2CBF3A4047802       C:\tes...

# To see the whole output we can pipe it to Format-List
PS C:\test> Get-FileHash .\process1.txt | Format-List
Algorithm : SHA256
Hash      : FDA966B28DB48262D48DBC1680268B5DE814F0D3E2BBFEC4F7C2CBF3A4047802
Path      : C:\test\process1.txt

# To use a different hashing algorithm use -Algorithm
PS C:\test> Get-FileHash .\process1.txt -Algorithm SHA384 | Format-List
Algorithm : SHA384
Hash      : DAFC5DFEC5E52441EFD4453D226486CAF011C2BCECF857690F2BC09AC1A7354E2D7E4D1935AB2CB92A82
            F485699C0CCA
Path      : C:\test\process1.txt
```

Different algorithms:

* SHA1
* SHA256
* SHA384
* SHA512
* MACTripleDES
* MD5
* RIPEMD160

It seems like it does not have one for strings.

### Select-String (almost like grep)
Unfortunately it cannot do recursive searching. (`-r` for `grep`).

```powershell
ls -Force -Filter *.txt -Recursive | Select-String "password"

# -Force -fo: Show hidden and system files.
# -Filter -fi *.txt: Show only txt files.
* -Recursive: -r
```

<!-- Links -->
[source-computerperformance]: http://www.computerperformance.co.uk/powershell/powershell_whatif_confirm.htm
