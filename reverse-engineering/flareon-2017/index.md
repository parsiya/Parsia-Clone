---
draft: false
toc: false
comments: false
categories:
- Reverse engineering
tags:
- CTF
title: "FlareOn 2017 CTF Notes"
wip: false
snippet: "Random notes from FlareOn 2017 Reverse Engineering CTF."
---


# Random notes from FlareOn-2017 Challenge

# 1 - login.html
Look inside `login.html`. It's ROT-13.

-----

# 2 - IgniteMe.exe
Simple x86 binary, looks like a bunch of XOR-es done on `byte_403000`.

Write the prompt and call `sub_4010F0` (it's not waiting for input yet).

F7: Step Into
F8: Step Over

``` c
var1 = 0
var8 = 0

if (var8 < 0x104) // 0x104 = 260
{
  ecx = var8
  ecx+Buffer = 0 // is it zero-ing out a 260 byte buffer?

  // eax = var8
  // eax++
  // var8 = eax

  var8++
}

*edx = NumberOfBytesRead = 0x98 = 152  // why is this not 0?
push *dex
push 0x104 = 206 // nNumberOfBytesToRead
push Buffer (260 char zero-ed out that we saw before)

ds:ReadFile = read from input and put into Buffer.

counter = var8 = 0 // var8 is reset

while (counter < strlen(Buffer))
{
  eax = Buffer

  push eax // push Buffer

  strlen(Buffer) // sub_401020(Buffer) see below

  if (strlen(Buffer) < 0) // function returns 0 if string is empty
  {
    // mov eax, 1
    // return
    return 1
  }
  else
  {
      // dl = Buffer[ecx]
      // var1 = dl
      // var1 = Buffer[ecx]
      
      // look for 0x0A
      // mov var1, eax
      // cmp eax, 0x0A

      // look for 0x0D
      // movzx  ecx, [ebp+var_1]
      // cmp     ecx, 0Dh
      // jz      short loc_4011A4

      // check for 0x00
      // movzx   edx, [ebp+var_1]
      // test    edx, edx
      // jz      short loc_4011A4
      
      if (Buffer[counter] != 0x0A || 0x0D || 0x00 ) // newline or end of string
      {
        // eax = var8 // ecx
        // cl = Buffer[ecx]
        // byte_403078[eax] = cl // Copy buffer to byte_403078 but bypass new those 3 chars
        byte_403078[counter] = Buffer[counter]
      }

      loc_4011A4:
      // edx = var8
      // edx++
      // var8 = edx
      counter++
    }
}
```

**Seems like it reads input and removes newlines and copies the rest to byte_403078.**


`sub_401020`

``` c
arg0 = Buffer
var4 = 0

loc_40102B:

eax = Buffer
eax = eax + var4 // 0

// movsx ecx, byte ptr [eax]
ecx = Buffer[0]

// test ecx, ecx
// jz short loc_401043

if (ecx == 0) goto loc_401043 // e.g. jmp there if we have reached the end of the string

// else

// edx = var4
// edx++
// var4 = edx

var4++

goto loc_40102B

loc_401043:

// eax = var4
// return

return var4
```

In other words it's just strlen(Buffer).

``` c
var4 = 0

while (Buffer[var4] != 0)
{
  var4++
}

return var4
```

Now let's look at `sub_401050`

``` c
push byte_403078  // cleaned string
varC = strlen(byte_403078)  // strlen(cleaned_string)

call sub_401000
eax = 0x00700004
var1 = al = 0x04

eax = varC // len(cleaned string)
eax--
var8 = eax // varC--

if (var8 < 0) // if (len(cleaned_string) - 1 < 0) aka if (len(cleaned_string) == 0)
{
  var8 = 0
  if (var8 < 0x27) // which obviously always happens
  {
    // eax = var8
    // ecx = xor_string[eax]
    // edx = var8
    // eax = target_string[var8]
    // cmp ecx, eax

    if (xor_string[var8] == target_string[var8])
    {
      var8++
    }
    else
    {
      return 0
    }
  }
}
else
{
  edx = var8
  eax = cleaned_string[var8] // in this case it's the last char (because null termination?)
  ecx = var1 // 0x04
  eax = eax xor ecx // last one is xor-ed by 0x04
  edx = var8
  mov byte_403180[edx], al // first char of xor_string = last char of cleaned_string xor 0x04
  var1 = cl // clearned_string[var8]

  var8--

  // next round the previous char is xor-ed with next one

  // in other words
  // parse the string in reverse
  // first char is xor-ed by 0x04
  // next chat is xor-ed by previous char in clearned_string
}
```

``` python
kstr1 = "0D2649452A1778442B6C5D5E45122F172B446F6E56095F454773260A0D1317484201404D0C0269"

str1 = str1.decode("hex")

result = ""

# key = unhexlify("04")
key = "04".decode("hex")

def xor2(plaintext, key):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(plaintext, key))

for char in str1[::-1]:
    key = xor2(key, char)
    result += key
    print key.encode('hex')

print result[::-1]

```

`sub_401000`

``` c
eax = 0x80070057
edx = eax = 0x80070057
xor ax, ax  // eax = 0x80070000 -- the first 4 bytes of eax (ax) is zero-ed
rol eax, 4  // eax = 0x00700008 -- remember it's rotate left by 4 bits (not bytes)
shr ax, 1   // eax = 0x00700004 -- remember shift-right by 1 bit on only ax (everything is replaced by 0 last one goes into CF but the rest fall off)

return eax 0x00700004
```

**flag: R_y0u_H0t_3n0ugH_t0_1gn1t3@flare-on.com**

-----

# 3 - greek_to_me.exe

Running strings (from Sysinternals) on it we get:

- `-nobanner`: do not display banner.
- `-o`: print the offset of the string (useful in case we want to use find the string in a hex editor like HxD).

```
PS > .\SysinternalsSuite\strings64.exe -o -nobanner .\3-GreektoMe\greek_to_me.exe
0077:!This program cannot be run in DOS mode.
0176:Rich
0432:.text
0472:.rdata
0526:SVW
0617:h0 @
0755:s|j
0759:j+hH @
0786:( @
0794:_^[
0824:$ @
0839:VWj
0851:  @
0860:tzht @
0911:t@h
0928:t/j
0986:( @
1015:tQS
1021:VWj
1095:_^[
1584:Nope, that's not it.
1608:Congratulations! But wait, where's my flag?
1652:127.0.0.1
1752:WS2_32.dll
```

`WS2_32.dll` is the Windows socket library. So network connectivity.

Here's some interesting info that I found when searching for it: https://nakedsecurity.sophos.com/2009/10/12/windows-ws232dll-file-safe/

Looking at `127.0.0.1` this means the application has network connectivity.

Initially I thought the application is trying to contact a local server. So I ran procmon and Wireshark (that can capture local loopback on Windows using `npcap` see https://wiki.wireshark.org/CaptureSetup/Loopback) and ran the application. I saw no `TCP/UDP Connect` events procmon or any local loopback traffic in Wireshark.

The app starts and then does nothing. If we run `netstat -anb`  in an Admin command prompt, we can see the app is listening on port `2222`.

```
 TCP    127.0.0.1:2222         0.0.0.0:0              LISTENING       5816
[greek_to_me.exe]
```

Or for example using `TCPView` for Sysinternals.

Supposedly we have to send a string of stuff to this socket.

## IDA

``` nasm
public start
start proc near
call    sub_401008
xor     eax, eax
retn
start endp
```

`sub_401008` is called, then app returns 0 and exits.

Inside `sub_401008` we see another subroutine `sub_401121`. Before that a `*buf` is pushed (as an argument) and is empty.

### sub_401121
We can see the socket being constructed.

``` nasm
lea     eax, [ebp+WSAData]
push    eax             ; lpWSAData
push    202h            ; wVersionRequested
call    ds:WSAStartup
test    eax, eax
jz      short loc_401147
```

Then if `WSAStartup` was successful we can see the port and other parameters being passed to `socket`. IDA highlights a lot of them of us.

``` nasm
loc_401147:
push    esi
push    edi
push    6               ; protocol
push    1               ; type
push    2
pop     edi
push    edi             ; af
call    ds:socket
mov     esi, eax
cmp     esi, 0FFFFFFFFh
jz      short loc_4011D8
```

We can see `socket` here. And of course the arguments are pushed to the stack from right to left.

- af = 2 = AF_INET = IPv4
- type = 1 = SOCK_STREAM = TCP socket
- protocol = 6 = IPPROTO_TCP = TCP

The address to bind to.

``` nasm
push    offset cp       ; "127.0.0.1"
mov     [ebp+name.sa_family], di
call    ds:inet_addr
```

https://msdn.microsoft.com/en-us/library/windows/desktop/ms738563(v=vs.85).aspx

The string "127.0.0.1" is being converted to an inet address.

Then port

``` nasm
push    8AEh            ; hostshort
mov     dword ptr [ebp+name.sa_data+2], eax
call    ds:htons
```

https://msdn.microsoft.com/en-us/library/windows/desktop/ms738557(v=vs.85).aspx

"The htons function converts a u_short from host to TCP/IP network byte order (which is big-endian)."

`0x8AE` is `2222` decimal.

Then bind

``` nasm
mov     word ptr [ebp+name.sa_data], ax
lea     eax, [ebp+name]
push    10h             ; namelen
push    eax             ; name
push    esi             ; s
call    ds:bind
```

https://msdn.microsoft.com/en-us/library/windows/desktop/ms737550(v=vs.85).aspx

"The bind function associates a local address with a socket."

After there is `listen`, `accept` and `recv` but we already know what they do.

Finally we are listening on `127.0.0.1:2222`.

Let's take a closer look at `recv`.

"The recv function receives data from a connected socket or a bound connectionless socket."

https://msdn.microsoft.com/en-us/library/windows/desktop/ms740121(v=vs.85).aspx

``` nasm
push    0               ; flags
push    4               ; len
push    [ebp+buf]       ; buf
push    edi             ; s
call    ds:recv
test    eax, eax
jle     short loc_4011CA
```

`Buf` from the parameter is going to be the pointer to the data received. `recv` returns the number of bytes received (which going to be in eax).

If nothing was received, the `jle` is successful and socket is closed.

Otherwise the function returns the number of received bytes.

**tl;dr**

`int bindAndListen(*buf)` listens on `127.0.0.1:2222`, data is in buf and returns the number of bytes received.

Seems like it receives (or processed data in 4 byte chunks) because ecx after leaving the function is pointing to only the first 4 bytes (and eax after recv was 4).

Now these parts are interesting.

``` nasm
loc_401029:
mov     ecx, offset loc_40107C
add     ecx, 79h
```

ecx after this is pointing to this place:

``` nasm
.text:004010F5 push    0                               ; flags
.text:004010F7 push    2Bh                             ; len
.text:004010F9 push    offset aCongratulation          ; "Congratulations! But wait, where's my flag?"
.text:004010FE push    [ebp+s]                         ; s
.text:00401101 call    ds:send
```
Then this one is misleading. Seems like this is data but IDA thinks it's code. Let's play along for now.

``` nasm
mov     eax, offset loc_40107C
mov     dl, [ebp+buf]
```

Now dl points to the first byte that we sent to the socket.

``` nasm
loc_401039:
mov     bl, [eax]         ; bl = 0x33 (first byte there)
xor     bl, dl            ; bl = 0x33 xor our_first_byte
add     bl, 22h           ; bl += 0x22
mov     [eax], bl         ; *eax = bl
inc     eax               ; eax++ (next char?)
cmp     eax, ecx          ; ecx is the address of the second section
jl      short loc_401039  ; check if we have reached the next section
```

Seems like all that section is being XOR-ed with just the first byte that we sent (in this case 0x30).

To see data that is being XOR-ed (blob1), we can either grab it here or from a hex editor by opening the binary.

33 E1 C4 99 11 06 81 16 F0 32 9F C4 91 17 06 81 14 F0 06 81 15 F1 C4 91 1A 06 81 1B E2 06 81 18 F2 06 81 19 F1 06 81 1E F0 C4 99 1F C4 91 1C 06 81 1D E6 06 81 62 EF 06 81 63 F2 06 81 60 E3 C4 99 61 06 81 66 BC 06 81 67 E6 06 81 64 E8 06 81 65 9D 06 81 6A F2 C4 99 6B 06 81 68 A9 06 81 69 EF 06 81 6E EE 06 81 6F AE 06 81 6C E3 06 81 6D EF 06 81 72 E9 06 81 73 7C

blob2 = (blob xor first_byte) + 0x22

CyberChef recipe for this (assuming our first byte is 0x30) is (remember you have to have one space after the last hex byte in input):

```
From_Hexdump()
XOR({'option':'Hex','string':'30'},'Standard',false)
ADD({'option':'Hex','string':'22'})
To_Hex('Space')
To_Upper_case('All')
```

blob2 (with first byte 0x30)

```
25 F3 16 CB 43 58 D3 48 E2 24 D1 16 C3 49 58 D3 46 E2 58 D3 47 E3 16 C3 4C 58 D3 4D F4 58 D3 4A E4 58 D3 4B E3 58 D3 50 E2 16 CB 51 16 C3 4E 58 D3 4F F8 58 D3 74 01 58 D3 75 E4 58 D3 72 F5 16 CB 73 58 D3 78 AE 58 D3 79 F8 58 D3 76 FA 58 D3 77 CF 58 D3 7C E4 16 CB 7D 58 D3 7A BB 58 D3 7B 01 58 D3 80 00 58 D3 81 C0 58 D3 7E F5 58 D3 7F 01 58 D3 64 FB 58 D3 65 6E
```

Then a new function is called.

``` nasm
mov     eax, [4198524]
mov     [ebp+var_C], eax  ; varC points to blob2 now
push    79h
push    [ebp+var_C]
call    sub_4011E6  ; sub_4011E6(blob2, 0x79)
pop     ecx
pop     ecx
movzx   eax, ax
cmp     eax, 0FB5Eh
jz      short loc_40107C
```

### sub_4011E6
arg4 = blob2_len = 0x79 = 121 = length of blob1 and blob2
arg0 = blob2

initial part before loops


blob2 in blocks of 20

```
25 F3 16 CB 43 58 D3 48 E2 24 D1 16 C3 49 58 D3 46 E2 58 D3 
47 E3 16 C3 4C 58 D3 4D F4 58 D3 4A E4 58 D3 4B E3 58 D3 50 
E2 16 CB 51 16 C3 4E 58 D3 4F F8 58 D3 74 01 58 D3 75 E4 58 
D3 72 F5 16 CB 73 58 D3 78 AE 58 D3 79 F8 58 D3 76 FA 58 D3 
77 CF 58 D3 7C E4 16 CB 7D 58 D3 7A BB 58 D3 7B 01 58 D3 80 
00 58 D3 81 C0 58 D3 7E F5 58 D3 7F 01 58 D3 64 FB 58 D3 65 
6E
```

If we go by blocks of 20, one last byte will remain.



``` nasm
edx  = 0x79 = size of blob2
ecx  = 0xFF
var4 = 0xFF
eax  = 0x14 = 20 decimal = block size
```

init done

``` c
di = var4

esi = edx

if (edx > eax) // if remaining data > block size use blocksize, otherwise use remaining data in blob2
{
  esi = eax  // cmova esi, eax
}

edx = edx - esi // remove one block from size of remaining data


// initial values
var4 = 0xFF
ecx  = 0xFF

// for each block do these
di = var4

for (i=0; i<esi; i++)
{
  di = di + blob2[i]
  var4 = di
  ecx = ecx + di
}

ax = first byte of var4
shr di, 8 // shift right one byte. In case of di, second byte is zero-ed and replaces first byte (e.g. 0B 25 >  00 0B)
          // in other worde divide di by 256
ax = ax + di
eax = ax // doesn't matter
var4 = eax // this overwrites all of var4 (remember we only copied the first byte)
eax = cl (only first byte of ecx from last while is saved)
shr cx, 8 (shift cx right one byte) // cx = cx / 8
ax = ax + cx
ecx = ax
eax = 0x14  // reset block size

```

After all these

``` nasm
loc_40124A:
movzx   edx, byte ptr [ebp+var_4]
mov     eax, ecx
shl     ecx, 8
and     eax, 0FF00h
add     eax, ecx
mov     cx, word ptr [ebp+var_4]
shr     cx, 8
add     dx, cx
or      ax, dx
mov     esp, ebp
pop     ebp
retn
```

Seems like it does not matter, the function returns eax which only first 2 bytes are populated.

Which means in the end we will only have 65535 different combinations.

---------

### After sub_4011E6

0x00 = 2597

0x79 = 21D3


What we want is, blob2 to be valid x86 instructions.

So we want to bruteforce all the XORs



Works for `A2`. 

See `fuzz5.py` for WinAppDbg in-memory brute force.

We could have just created a Python program.

1. Run the application.
2. Send a byte.
3. Print the response.
4. Go to 1.

But I learned WinAppDbg, well kinda sorta.


**flag: et_tu_brute_force@flare-on.com**


-----

# 4 - Notepad.exe
Seems like we need a Windows 7 VM for this. I read that it crashed on Windows 10. That meant I had to setup a Windows 7 VM.

Dropping it in PEStudio gives us a bunch of information.

In Resource Hacker we see some dialog named "NPENCODINGDIALOG". I don't think I have ever seen it in real notepad. But I could be wrong. This is from the save dialog. You can set the encoding of the file. I am not sure why it's in a different location, could be normal.

Running it in procmon did not show anything special.

## In IDA
We can see a bunch of char strings being loaded in local variables. Put a breakpoint on `.rsrc:01013C49 call    $+5` and read the strings.

- `%USERPROFILE%`
- `\flareon2016challenge`
- `ImageHlp.dll`
- `CheckSumMappedFile`
- `user32.dll`
- `MessageBoxA`

It might be looking for a file.

Let's run procmon again but look for the `%USERPROFILE%` path which is `C:\Users\YouUser`.

Don't be fooled by looking for the `notepad.exe.local` file, it's a Windows thing https://blogs.msdn.microsoft.com/junfeng/2006/01/24/dotlocal-local-dll-redirection/.

Nothing is found, let's dig deeper.

After loading the strings, `sub_10153D0` is called.

The first thing it does is call `sub_10153C0` which is pretty simple.

``` nasm
sub_10153C0 proc near
mov     eax, large fs:30h
retn
sub_10153C0 endp
```

This functions returns the Process Environment Block (PEB).

This can be later used to get information like "isBeingDebugged."

Flare people like their Anti-debugging techniques.

https://parsiya.net/images/2014/flare/7-4.jpg

More info about PEB: https://www.aldeid.com/wiki/PEB-Process-Environment-Block

PEB is then stored in var4 and eax.

mov     ecx, [eax+0Ch]

Loads byte 12 (0x0C) of PEB into ecx. Which is `0x00c _PEB_LDR_DATA* Ldr;`.

According to this link https://www.aldeid.com/wiki/PEB_LDR_DATA it's:

"The PEB_LDR_DATA structure is a structure that contains information about all of the loaded modules in the current process."

``` c
typedef struct _PEB_LDR_DATA
{
    0x00    ULONG         Length;                            /* Size of structure, used by ntdll.dll as structure version ID */
    0x04    BOOLEAN       Initialized;                       /* If set, loader data section for current process is initialized */
    0x08    PVOID         SsHandle;
    0x0c    LIST_ENTRY    InLoadOrderModuleList;             /* Pointer to LDR_DATA_TABLE_ENTRY structure. Previous and next module in load order */
    0x14    LIST_ENTRY    InMemoryOrderModuleList;           /* Pointer to LDR_DATA_TABLE_ENTRY structure. Previous and next module in memory placement order */
    0x1c    LIST_ENTRY    InInitializationOrderModuleList;   /* Pointer to LDR_DATA_TABLE_ENTRY structure. Previous and next module in initialization order */
} PEB_LDR_DATA,*PPEB_LDR_DATA; // +0x24
```

``` nasm
mov     edx, [ecx+14h]
mov     [ebp+var_C], edx
mov     eax, [ebp+var_C]
mov     [ebp+var_8], eax
```

Then byte 20 (0x14) is loaded into edx. According to our source this is `InMemoryOrderModuleList`.

https://msdn.microsoft.com/en-us/library/windows/desktop/aa813708(v=vs.85).aspx

"The head of a doubly-linked list that contains the loaded modules for the process. Each item in the list is a pointer to an LDR_DATA_TABLE_ENTRY structure. For more information, see Remarks."

So the process wants to enumerate all loaded modules.

Loaded into varC and then var8.

``` nasm
mov     ecx, [ebp+var_C]
mov     edx, [ecx+28h]
push    edx
call    sub_1015270
```

Byte 40 is pushed to stack to be called for `sub_1015270`. If I am not mistaken it's `FullDllName`.

``` c
typedef struct _LDR_DATA_TABLE_ENTRY {
    PVOID Reserved1[2];
    LIST_ENTRY InMemoryOrderLinks;
    PVOID Reserved2[2];
    PVOID DllBase;
    PVOID EntryPoint;
    PVOID Reserved3;
    UNICODE_STRING FullDllName;
    BYTE Reserved4[8];
    PVOID Reserved5[3];
    union {
        ULONG CheckSum;
        PVOID Reserved6;
    };
    ULONG TimeDateStamp;
} LDR_DATA_TABLE_ENTRY, *PLDR_DATA_TABLE_ENTRY;
```

With `LIST_ENTRY` being 8 bytes in a 32-bit binary (a struct of 2 pointers).

``` c
typedef struct _LIST_ENTRY {
   struct _LIST_ENTRY *Flink;
   struct _LIST_ENTRY *Blink;
} LIST_ENTRY, *PLIST_ENTRY, *RESTRICTED_POINTER PRLIST_ENTRY;
```

But we do not need any of these.

Later we see:

``` nasm
push    edx
call    sub_1015270
```

edx here is `filename` which in our case `notepad.exe`. Remember it's unicode so we will see `00` between characters. `0` in ASCII-HEX is `0x30` but in Unicode it's `0x0030`.

So we are running `sub_1015270("notepad.exe")`.

### sub_1015270

``` 
before loop:
var4 = 0

for char in filename:
  edx  = var4
  edx  = edx shr 0x0D
  eax  = var4
  eax  = eax shl 0x13
  edx  = edx or eax
  var4 = edx
  ecx  = var4
  ecx  = ecx add char
  var4 = ecx
```

We want this calculation done on filename to be the same result as `0x8FECD63F`.

In case of `notepad.exe` it will be `0xD589DE91`.

The thing that I initially missed was that this iterates over the names of all loaded modules so it's looking for a specific module.

I thought we needed the file to have a specific name that resulted in that result.

But the address space is pretty big. Assuming we have 7 spaces and each char could one of 80. It will be 80^7 or 20+ billion.

``` nasm
loc_10153F0:
mov     ecx, [ebp+var_C]
mov     edx, [ecx+28h]
push    edx
call    sub_1015270
cmp     eax, [ebp+arg_0]
jnz     short loc_101540B
```

Change `eax` to `0x8FECD63F` and continue.

Then we get to

``` nasm
mov     eax, [ebp+var_C] ; <--- put a breakpoint here and run until this triggers.
mov     eax, [eax+10h]
jmp     short loc_1015424
```
varC is `InMemoryOrderModuleList` and byte 0x10 of it is `PVOID DllBase;`

Now we can look to the right in IDA under `Modules` and find out what module satisfied the constraint.

It was loading `C:\Windows\syswow64\kernel32.dll (Base) 77430000 (Size) 00110000`


Each pointer is 4 bytes.

``` c
typedef struct _LDR_DATA_TABLE_ENTRY {
    PVOID Reserved1[2];
    LIST_ENTRY InMemoryOrderLinks;
    PVOID Reserved2[2];
    PVOID DllBase;      // +0x10
    PVOID EntryPoint;
    PVOID Reserved3;
    UNICODE_STRING FullDllName;
    BYTE Reserved4[8];
    PVOID Reserved5[3];
    union {
        ULONG CheckSum;
        PVOID Reserved6;
    };
    ULONG TimeDateStamp;
} LDR_DATA_TABLE_ENTRY, *PLDR_DATA_TABLE_ENTRY;
```

In this case `DllBase` is `0x77430000`.

**Back to Main**

var1EC = 0x77430000

`sub_1015310(0x77430000, 0x63D6C065)`

### sub_1015310(Dllbase, 0x63D6C065)

var10 = arg0 = DllBase = 77430000

var1C = 77430000 + [0x7743003C] = 774300E8

What is at byte `0x3C` of `kernel32.dll`?

That is the pointer that points to the start of PE header.

"At offset 60 (0x3C) from the beginning of the DOS header is a pointer to the Portable Executable (PE) File header (e_lfanew in MZ structure). DOS will print the error message and terminate, but Windows will follow this pointer to the next batch of information."

Source: https://en.wikibooks.org/wiki/X86_Disassembly/Windows_Executable_Files#PE_Header

Seems like we are trying to jump over the DOS header.

ecx = 0x77430000

add     ecx, [eax+78h]

eax points to the start of the PE header (e.g. the chars PE). What is at offset `0x78` of PE? In other words offset `0x160` of DLL. In this case it's `0xE0`.

var18 = ecx = 0x774F01E0 and according to IDA this points to `kernel32_NlsUpdateSystemLocale+C8E`.

This keeps reading and reading. We need to go down and see what happens in the end.

We take the first left branch

``` nasm
.rsrc:01015384 mov     edx, [ebp+var_20]
.rsrc:01015387 push    edx      ; <--- "acquireSRW"
.rsrc:01015388 call    sub_10152C0
.rsrc:0101538D cmp     [ebp+arg_4], eax
```

sub_10152C0 with acquiresSRW return `0xA77D8D5A`.

Return result of this function is `0x7744E296` which points to `kernel32_FindFirstFileA`.

**Back to Main**

var78 = 0x7744E296 = kernel32_FindFirstFileA

var74 = 0x7746D56E = kernel32_FindNextFileA

**Let's go back and run procmon again.**

This time we add a new filter `Result is NAME NOT FOUND`.

We see this line:

```
5:15:14.7189299 AM  notepad.exe 3444  IRP_MJ_CREATE C:\Users\x64\flareon2016challenge NAME NOT FOUND  Desired Access: Read Data/List Directory, Synchronize, Disposition: Open, Options: Directory, Synchronous IO Non-Alert, Attributes: n/a, ShareMode: Read, Write, Delete, AllocationSize: n/a
```

We have already seen this string at the start.

Let's create this directory and run it again.

Seems like it's trying to list everything in the directory now (don't forget to remember the result filter in procmon).

```
5:19:02.2219578 AM  notepad.exe 3472  IRP_MJ_CREATE C:\Users\x64\flareon2016challenge SUCCESS Desired Access: Read Data/List Directory, Synchronize, Disposition: Open, Options: Directory, Synchronous IO Non-Alert, Attributes: n/a, ShareMode: Read, Write, Delete, AllocationSize: n/a, OpenResult: Opened
5:19:02.2219763 AM  notepad.exe 3472  IRP_MJ_DIRECTORY_CONTROL  C:\Users\x64\flareon2016challenge\* SUCCESS Type: QueryDirectory, Filter: *, 2: .
5:19:02.2219907 AM  notepad.exe 3472  IRP_MJ_DIRECTORY_CONTROL  C:\Users\x64\flareon2016challenge SUCCESS Type: QueryDirectory, 1: ..
5:19:02.2219999 AM  notepad.exe 3472  IRP_MJ_DIRECTORY_CONTROL  C:\Users\x64\flareon2016challenge NO MORE FILES Type: QueryDirectory
5:19:02.2220071 AM  notepad.exe 3472  IRP_MJ_CLEANUP  C:\Users\x64\flareon2016challenge SUCCESS 
5:19:02.2220138 AM  notepad.exe 3472  IRP_MJ_CLOSE  C:\Users\x64\flareon2016challenge SUCCESS 
```

Let's put a couple of files there and try again. nem1.txt and nem2.txt.

We can see that it reads the files. It's probably listing the directory, going through all files and looking for something.

```
12:54:29.8193558 PM notepad.exe 932 IRP_MJ_CREATE C:\Users\x64\flareon2016challenge\nem1.txt  SUCCESS Desired Access: Generic Read/Write, Disposition: Open, Options: Synchronous IO Non-Alert, Non-Directory File, Attributes: N, ShareMode: None, AllocationSize: n/a, OpenResult: Opened
```

This is where the file is being read. Double click on it and go to the stack tab. We can see where it's being called.

```
22  notepad.exe notepad.exe + 0x14e54 0x1014e54 C:\Users\x64\Desktop\4-notepad\notepad.exe
23  notepad.exe notepad.exe + 0x14290 0x1014290 C:\Users\x64\Desktop\4-notepad\notepad.exe
24  notepad.exe notepad.exe + 0x13efa 0x1013efa C:\Users\x64\Desktop\4-notepad\notepad.exe
```

### sub_1014E20


var44 = CreateFileA(FileInDirectory)
var38 = GetFileSize(var44)
var40 = CreateFileMapping(var44)
var4C = MapViewOfFile(var44)

#### MapViewOfFile
If the function succeeds, the return value is the starting address of the mapped view.

An application can treat a memory mapped file like memory. Meaning it can read and write on it like memory while the file is actually on disk.

For more info see here: https://msdn.microsoft.com/en-us/library/ms810613.aspx under `What Are Memory-Mapped Files?`

### Back to sub_1014E20

``` nasm
rsrc:01014EAD loc_1014EAD:                 ; CODE XREF: sub_1014E20+77
.rsrc:01014EAD push    0
.rsrc:01014EAF push    0
.rsrc:01014EB1 push    0
.rsrc:01014EB3 push    2
.rsrc:01014EB5 mov     edx, [ebp+var_40]
.rsrc:01014EB8 push    edx
.rsrc:01014EB9 mov     eax, [ebp+arg_0]
.rsrc:01014EBC mov     ecx, [eax+18h]
.rsrc:01014EBF call    ecx                  ; MapViewOfFile
.rsrc:01014EC1 mov     [ebp+var_4C], eax    ; handle to file
.rsrc:01014EC4 mov     edx, [ebp+var_4C]
.rsrc:01014EC7 movsx   eax, word ptr [edx]  ; first two bytes (e.g. word) are read and put in eax
.rsrc:01014ECA cmp     eax, 5A4Dh
.rsrc:01014ECF jz      short loc_1014EFC
```

The result of MapViewOfFile is passed to var4C. First two bytes are moved to eax and then compared with `0x5A4D`. Remember that the first char goes into the lower bytes so it's looking for a file that starts with `4D 5A`. This is the classic `MZ` header. Is it looking for a executable?

Let's change our first file and add `MZ` to its start.

``` nasm
loc_1014EFC:
mov     ecx, [ebp+var_4C]   ; ecx = handle to file
mov     [ebp+var_1C], ecx
mov     edx, [ebp+var_1C]
mov     eax, [edx+3Ch]      ; load byte 0x3C of the file into eax
cmp     eax, [ebp+var_38]   ; var38 = FileSize
jge     short loc_1014F51
```

We already know what's at `0x3C` of PE. That is the pointer that points to the start of PE header. Not this is actually 4 bytes (e.g. you will see `3C 00 00 00`). In this case (and probably in most cases this is just a single byte. If this says `0xF0` you go to that offset in file and get the PE header.

It's checking that the pointer is larger than filesize. In other words, it's trying to detect if it's a legit executable file (or a fake file like ours which only has the first few bytes in the header).

### PE Header detour
This is probably the best resource out there for it. https://msdn.microsoft.com/en-us/library/ms809762.aspx

This is also good because it details the different fields and other stuff: https://www.curlybrace.com/archive/PE%20File%20Structure.pdf

More info (this is why app uses imagehlp.dll): https://msdn.microsoft.com/en-us/library/windows/desktop/ms680547(v=vs.85).aspx

I am going to come back up here and update the info.

We will use `calc.exe` (Windows 7 version) as example.

#### MZ Header

```
00000000  4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00  |MZ..........ÿÿ..|
00000010  b8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00  |¸.......@.......|
00000020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  |................|
00000030  00 00 00 00 00 00 00 00 00 00 00 00 f0 00 00 00  |............ð...|
```

The fields we are interested in are:

- MZ header: `4D5A` or `MZ`
- Last page size: `0090`
- Total pages in file: `0003`
- Pointer to PE header: `000000F0` (at `0x3C`)


#### PE Header
You can view the PE header in `PE Studio` under `File header`.

Also see this https://github.com/zed-0xff/pedump. The example in readme is calc.exe which is what we are using.

```
00000000  50 45 00 00 64 86 06 00 d4 c9 5b 4a 00 00 00 00  |PE..d...ÔÉ[J....|
00000010  00 00 00 00 f0 00 22 00 0b 02 09 00 00 0e 06 00  |....ð.".........|
00000020  00 f2 07 00 00 00 00 00 b8 b9 01 00 00 10 00 00  |.ò......¸¹......|
00000030  00 00 00 00 01 00 00 00 00 10 00 00 00 02 00 00  |................|
```

First 4 bytes are the PE signature (or header whatever) 
- 00: `504500` - PE signature `PE 00 00`

Then we have the Image file header. See here for everything: https://msdn.microsoft.com/en-us/library/windows/desktop/ms680313(v=vs.85).aspx

``` c
typedef struct _IMAGE_FILE_HEADER {
  WORD  Machine;
  WORD  NumberOfSections;
  DWORD TimeDateStamp;
  DWORD PointerToSymbolTable;
  DWORD NumberOfSymbols;
  WORD  SizeOfOptionalHeader;
  WORD  Characteristics;
} IMAGE_FILE_HEADER, *PIMAGE_FILE_HEADER;
```
- 04: `86 64`       - `Machine`. In this case it means x64 (IMAGE_FILE_MACHINE_AMD64). `01 4C`: x86 - `02 00` Intel Itanium (IA64).
- 06: `00 06`       - Number of sections.
- 08: `4A 5B C9 D4` - "The low 32 bits of the time stamp of the image. This represents the date and time the image was created by the linker." In this case the timestamp is `Mon 13 July 2009 23:57:08 UTC`.
    - The recipe in CyberChef is (if you copy paste the bytes from hex editor):

        ``` json
        [
          { "op": "Swap endianness",
            "args": ["Hex", 4, true] },
          { "op": "From Base",
            "args": [16] },
          { "op": "From UNIX Timestamp",
            "args": ["Seconds (s)"] }
        ]
        ```

### Back to sub_1014E20

**Perhaps it's trying to execute one of the files from the previous year's challenge.**

Now this works for our small 4-5 char file because there's nothing at that location and it returns 0. 0 is smaller than filesize so it passes the check.

``` nasm
.rsrc:01014F0D mov     ecx, [ebp+var_1C]
.rsrc:01014F10 mov     edx, [ebp+var_4C]
.rsrc:01014F13 add     edx, [ecx+3Ch]
.rsrc:01014F16 mov     [ebp+var_5C], edx
.rsrc:01014F19 mov     eax, [ebp+var_5C]
.rsrc:01014F1C cmp     dword ptr [eax], 4550h
.rsrc:01014F22 jz      short loc_1014F4F
```

Next check is simple. It checks if the data at the start of the PE header is actually `0x4550` (or PE)

Let's restart but put an actual executable in the directory. I used `calc.exe`.

``` nasm
.rsrc:01014F7C
.rsrc:01014F7C loc_1014F7C:           ; CODE XREF: sub_1014E20:loc_1014F4F
.rsrc:01014F7C mov     ecx, [ebp+var_5C]
.rsrc:01014F7F movzx   edx, word ptr [ecx+4]
.rsrc:01014F83 cmp     edx, 14Ch
.rsrc:01014F89 jnz     short loc_1014F97
```

var5C is start of PE header (from last check).

It checks if bytes 4 and 5 (starting from 0) after PE header are `0x4C` and `0x01`. See above in PE header for explanation. This is checking if this is a x86 executable. In our case, calc is for a 64-bit machine so it will read `86 64` (`64 86` in hex editor). For now we can just change it and see what happens later.


``` nasm
mov     eax, [ebp+var_5C]
movzx   ecx, word ptr [eax+16h]
and     ecx, 2
jnz     short loc_1014FC2
```

Then it loads the byte at PEHeader+22 (`0x16`) and ands it with 2, if the result is zero we take the bad path. For calc it's `0x22` and we are safe. The only time something AND 2 is not zero, is when the first two bits of the byte at that number are not 11.

``` nasm
loc_1014FC2:
mov     edx, [ebp+var_4C]   ; push *file
push    edx
mov     eax, [ebp+var_5C]   ; push *PEHeader
push    eax
mov     ecx, [ebp+arg_0]    ; push arg0 
push    ecx
call    sub_10146C0
mov     [ebp+var_50], eax
cmp     [ebp+var_50], 2
jz      short loc_1015008
```

### sub_10146C0
Bunch of new strings at start.

* `\key.bin`
* `%USERPROFILE%`
* `\flareon2016challenge`
* ` ` (space or 0x20)
* `where's my key file?`
* `what's wrong with my key file?`
* `37E7D8BE7A533025BB38572697266F50F47567BFB0EFA57A65AEAB6673A0A3A140F60C` this byte sequence

Then this function is called `kernel32_ExpandEnvironmentStringsA`

https://msdn.microsoft.com/en-us/library/windows/desktop/ms724265(v=vs.85).aspx

Changes the value of an environment-variable for the current user.

``` cpp
DWORD WINAPI ExpandEnvironmentStrings(
  _In_      LPCTSTR lpSrc,
  _Out_opt_ LPTSTR  lpDst,
  _In_      DWORD   nSize
);
```

In this case it's called like this `ExpandEnvironmentStrings(%USERPROFILE% ,0x0CF86C , 0x104)`

Seems like it could not modify the variable.

var244 = var240 = "\flareon2016challenge"

Then we go through the previous string. Nothing is changed.

``` nasm
loc_1014A00:
mov     eax, [ebp+var_240]
mov     cl, [eax]
mov     [ebp+var_245], cl
add     [ebp+var_240], 1
cmp     [ebp+var_245], 0
jnz     short loc_1014A00
```

Same thing happens to `c:\users\x64` or value of %USERPROFILE%.

We see the string `%USERPROFILE%\flareon2016challenge\key.bin` being formed. This is likely the name of the key file.

Then it loads up ~~calc~~ notepad.exe (the file that is being executed). Loads 4 bytes (dword) at `*PEHeader+8` and compares them to `0x48025287`.

This timestamp corresponds to `Mon 13 July 2009 23:57:08 UTC`. Which the timestamp of the original notepad.exe file.

See: https://gchq.github.io/CyberChef/#recipe=From_Base(16)From_UNIX_Timestamp('Seconds%20(s)')&input=NDgwMjUyODc

Then it checks the timestamp of the executable in the directory against `57D1B2A2`.

Next check is against `57D1B2A2` or `Thu 8 September 2016 18:49:06 UTC`:

``` nasm
mov     ecx, [ebp+arg_4]
cmp     dword ptr [ecx+8], 57D1B2A2h  ; remember endian-ness. In hex editor you will see A2 B2 D1 57
jnz     short loc_1014BC3
```

Let's modify the timestamp of calc.exe to that.

This time do not debug and just run notepad.exe with the modified calc.exe in the binary.

We get a timestamp with this `2016/09/08 18:49:06 UTC`.

Which is the same as the timestamp of modified calc.exe. This corresponds to the next check that says we need to change the timestamp of notepad.exe to that.

But before that let's go a bit down that rabbit hole.

Running procmon we can see that the rest of the files in the directory are still accessed. Maybe we are missing something.

It actually writes to the files. It writes something from the executable (in the case of our calc it's L32.DLL0x00 which is 8 bytes). It writes it 5 times into the key file (appends it if that matters). It writes 8 bytes from offset 0x400 of calc.

Let's get the `flareon2016challenge.dll` from the last year and try it. It seems like we need to change the timestamp though.

Run notepad, we get the thing. Inside the newly created keyfile we see `55 8B EC 83 EC 10 83 7D`. This is at offset 0x400 of the DLL.

But what if we put a copy of notepad.exe there, change the timestamp and ran the original.

With notepad we get `EF 6F DD 77 17 6C DD 77`.

If we change the timestamp of notepad.exe to that, we get to a branch where the timestamp of calc is checked against `Fri 9 September 2016 12:54:16 UTC` or `57D2B0F8`. If we do so, we will get a message box with `2016/09/09 12:54:16 UTC` (which is the same as the timestamp).

This time 8 bytes from offset 0x410 are appended to the key file.

Now we need to change the notepad timestamp to `57D2B0F8` but we are in IDA and we can just move around.

Just by looking at code we should understand that this time 8 bytes from offset 0x420 are copied to bin.


Next one is `579E9100` which copies 8 bytes from offset 0x430. `2016/08/01 00:00:00 UTC`

And finally everything in the key file gets XOR-ed with that string and shown in the message box.

``` nasm
loc_1014D19:
mov     edx, [ebp+var_204]
cmp     dword ptr [edx+8], 579E9100h
jnz     loc_1014E09
```

This time stamp is `Mon 1 August 2016 00:00:00 UTC`. 

https://gchq.github.io/CyberChef/#recipe=Swap_endianness('Hex',4,true)From_Base(16)From_UNIX_Timestamp('Seconds%20(s)')&input=MDAgOTEgOUUgNTc

Now it calls `CreateFileA` and looks for `key.bin`. Because it does not exist, it will take the bad path.

``` nasm
.rsrc:01014D2C push    0
.rsrc:01014D2E push    80h
.rsrc:01014D33 push    3
.rsrc:01014D35 push    0
.rsrc:01014D37 push    0
.rsrc:01014D39 push    80000000h
.rsrc:01014D3E lea     eax, [ebp+var_170]
.rsrc:01014D44 push    eax
.rsrc:01014D45 mov     ecx, [ebp+arg_0]
.rsrc:01014D48 mov     edx, [ecx+10h]
.rsrc:01014D4B call    edx
.rsrc:01014D4D mov     [ebp+var_60], eax
.rsrc:01014D50 cmp     [ebp+var_60], 0FFFFFFFFh
.rsrc:01014D54 jnz     short loc_1014D83
```

Looking back at the MSDN link for CreateFile we can see what is being pushed.

``` c
CreateFile(hTemplateFile = 0,
    dwFlagsAndAttributes = 0x80, // FILE_ATTRIBUTE_NORMAL - The file does not have other attributes set. This attribute is valid only if used alone.
    dwCreationDisposition= 0x03, // OPEN_EXISTING
    lpSecurityAttributes = 0,    // The handle returned by CreateFile cannot be inherited by any child processes the application
    dwShareMode          = 0,    // Prevents other processes from opening a file or device if they request delete, read, or write access.
    dwDesiredAccess= 0x80000000, // FILE_FLAG_WRITE_THROUGH - No caching - Write operations will go directly to disk.
    lpFileName           = "...\\flareon2016challenge\\key.bin"
    )
```

Handle to the key file goes into var60.

``` nasm
loc_1014D83:
push    0
lea     ecx, [ebp+var_18]
push    ecx
push    20h
lea     edx, [ebp+var_44]
push    edx
mov     eax, [ebp+var_60]
push    eax
mov     ecx, [ebp+arg_0]
mov     edx, [ecx+60h]
call    edx             ; ReadFile
cmp     [ebp+var_18], 20h
jz      short loc_1014DCB
```

``` c

BOOL WINAPI ReadFile(
  _In_        HANDLE       hFile,                // var60 - file handle to key.bin
  _Out_       LPVOID       lpBuffer,             // var44 - pointer to an empty buffer?
  _In_        DWORD        nNumberOfBytesToRead, // 0x20  - 32 decimal
  _Out_opt_   LPDWORD      lpNumberOfBytesRead,  // var18 - which looks like an empty buffer
  _Inout_opt_ LPOVERLAPPED lpOverlapped          // 0
);
```
So it reads 32 bytes from the key file.

Let's put some text into the key file and re-run.

`012345678901234567890123456789AB`

Then it checks if we read 0x20 bytes which we did.

push 0x20
push 
push 0x20
push `37E7D8BE7A533025BB38572697266F50F47567BFB0EFA57A65AEAB6673A0A3A140F60C` (remember start of the function?)

``` nasm
loc_1014DCB:
push    20                ; most likely the number of bytes we read from key.bin
lea     ecx, [ebp+var_44]
push    ecx               ; contents we just read from key.bin
push    20h
lea     edx, [ebp+var_200]
push    edx               ; 37E7D8BE7A533025BB38572697266F50F47567BFB0EFA57A65AEAB6673A0A3A140F60C
call    sub_1014670
```

### sub_1014670

var4 = 0
cmp with arg4 = 0x20

check if we read 32 bytes.

var4 = 0 ; counter?

edx = *arg0 = or *string
ecx = string[var4]
eax = var4

cdq = double the size of EAX. Then we will have EDX:EAX to represent stuff.

idiv edx:eax / argC (last 0x20)

In this case 0/32 result will be zero.

I will like that we are just doing some normal string operations and this is standard compiler code. I have seen this before but I don't remember. It's probably just going through the string and parse it.

eax = *keybin
edx = *keybin[0]

ecx = ecx xor edx (xor first byte of key with first byte of string)

store the result in string

This function just xors byte read from keybin with string (but seems like only does it for 32 bytes). So the last 3 bytes of *string will be untouched.


push 0
push *var4 = 0x20
push xor-ed string (with last 3 bytes untouched)
push 0

Call MessageBox and show the result

So `37E7D8BE7A533025BB38572697266F50F47567BFB0EFA57A65AEAB6673A0A3A1` gets XOR-ed with 32 bytes in the key.bin file and a message box shows the results.

Now it did not work with notepad. What about the challenge DLL from last year?

The bytes are `55 8B EC 83 EC 10 83 7D 05 00 00 8D 4A 02 2B D7 8D 77 02 89 55 F4 EB 08 8B 55 F4 0F B6 14 32 0F`

And the message box is still garbled although the first 4 bytes look readable `bl4=`.

------------

Ok I have been blind.

We have four timestamps. Look inside last year's challenge and find files with the same timestamp.

CyberChef example: https://gchq.github.io/CyberChef/#recipe=From_Base(16)From_UNIX_Timestamp('Seconds%20(s)')&input=NDkxODAxOTI

Make sure to either read the timestamp from a hex editor or use something like PEStudio because the one you see in Windows might not be what you are looking for.

- `57D1B2A2` - `Thu 8 September 2016 18:49:06 UTC` - challenge1.exe
- `57D2B0F8` - `Fri 9 September 2016 12:54:16 UTC` - DudeLocker.exe (challenge 2)
- `49180192` - `Mon 10 November 2008 09:40:34 UTC` - khaki.exe (challenge 6)
- `579E9100` - `Mon 1 August 2016 00:00:00 UTC`    - unknown (challenge 3) - Note PEStudio shows the timestamp as July 31st 00.

Now we need to see which challenge has this timestamp(s) and copy them (or grab the bytes from offset). See they are also sorted alphabetically based on the original files names.

55 8B EC 8B 4D 0C 56 57
8B 55 08 52 FF 15 30 20
C0 40 50 FF D6 83 C4 08
00 83 C4 08 5D C3 CC CC

And after the xor we get 

**bl457_fr0m_th3_p457@flare-on.com**


----------

# 5 - pewpewboat
Actually an ELF binary.

We need to setup remote debugging.

Setup two VMs, add an "internal network" card for each with the name `intnet` (or whatever).

Then the following command sets up DHCP for that. Now they can talk to each other.

```
C:\Program Files\Oracle\VirtualBox>VBoxManage dhcpserver add --netname intnet --ip 192.168.133.100 --netmask 255.255.255.0 --lowerip 192.168.133.101 --upperip 192.168.133.254 --enable
```

## recon

### Strings
We got some stuff from strings, some of them look interesting or could be anything.

```
allsunk!H9
__libc_start_main
GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609
```

### file

```
root@kali:~/Desktop/pewpew# file pewpewboat 
pewpewboat: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=580d3cee15362410c9e7b0ae44d65d57deb52912, stripped
```

### ldd

```
root@kali:~/Desktop/pewpew# ldd pewpewboat 
  linux-vdso.so.1 (0x00007fffdd3c4000)
  libtinfo.so.5 => /lib/x86_64-linux-gnu/libtinfo.so.5 (0x00007f9b2f977000)
  libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f9b2f5d9000)
  /lib64/ld-linux-x86-64.so.2 (0x000055fc98ef3000)
```

### nm

```
root@kali:~/Desktop/pewpew# nm pewpewboat 
nm: pewpewboat: no symbols
```

### readelf

```
root@kali:~/Desktop/pewpew# readelf -l pewpewboat 

Elf file type is EXEC (Executable file)
Entry point 0x400ae0
There are 9 program headers, starting at offset 64

Program Headers:
  Type           Offset             VirtAddr           PhysAddr
                 FileSiz            MemSiz              Flags  Align
  PHDR           0x0000000000000040 0x0000000000400040 0x0000000000400040
                 0x00000000000001f8 0x00000000000001f8  R E    0x8
  INTERP         0x0000000000000238 0x0000000000400238 0x0000000000400238
                 0x000000000000001c 0x000000000000001c  R      0x1
      [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
  LOAD           0x0000000000000000 0x0000000000400000 0x0000000000400000
                 0x00000000000046fc 0x00000000000046fc  R E    0x200000
  LOAD           0x0000000000004e00 0x0000000000604e00 0x0000000000604e00
                 0x000000000000e43c 0x000000000000e458  RW     0x200000
  DYNAMIC        0x0000000000004e18 0x0000000000604e18 0x0000000000604e18
                 0x00000000000001e0 0x00000000000001e0  RW     0x8
  NOTE           0x0000000000000254 0x0000000000400254 0x0000000000400254
                 0x0000000000000044 0x0000000000000044  R      0x4
  GNU_EH_FRAME   0x0000000000003fa0 0x0000000000403fa0 0x0000000000403fa0
                 0x000000000000015c 0x000000000000015c  R      0x4
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RW     0x10
  GNU_RELRO      0x0000000000004e00 0x0000000000604e00 0x0000000000604e00
                 0x0000000000000200 0x0000000000000200  R      0x1

 Section to Segment mapping:
  Segment Sections...
   00     
   01     .interp 
   02     .interp .note.ABI-tag .note.gnu.build-id .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt .init .plt .plt.got .text .fini .rodata .eh_frame_hdr .eh_frame 
   03     .init_array .fini_array .jcr .dynamic .got .got.plt .data .bss 
   04     .dynamic 
   05     .note.ABI-tag .note.gnu.build-id 
   06     .eh_frame_hdr 
   07     
   08     .init_array .fini_array .jcr .dynamic .got 

```

### strace
We can run strace to see system calls. The following options help:

- `-i`: Prints IP at time of syscall - this helps a lot with setting breakpoint.
- `-s9999`: Do not cutout strings in function parameters.
- `-o outputfile`: Store the output in a file - helps with not having the strace output interfere with the game.

Let's look at the interesting parts.

```
[00007fe97405b4f7] execve("./pewpewboat", ["./pewpewboat"], [/* 43 vars */]) = 0
[00007ff8d202a619] brk(NULL)            = 0xae4000
[00007ff8d202b347] access("/etc/ld.so.nohwcap", F_OK) = -1 ENOENT (No such file or directory)

[00007ff8d202b2e7] open("/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3

[00007ff8d202b347] access("/etc/ld.so.nohwcap", F_OK) = -1 ENOENT (No such file or directory)
[00007ff8d202b2e7] open("/lib/x86_64-linux-gnu/libtinfo.so.5", O_RDONLY|O_CLOEXEC) = 3

[00007ff8d202b2e7] open("/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3

[00007ff8d1b24f72] fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 0), ...}) = 0
[00007ff8d1b25600] write(1, "Loading first pew pew map...\n", 29) = 29

[00007ff8d1b25380] open("/lib/terminfo/x/xterm-256color", O_RDONLY) = 3
[00007ff8d1b255a0] read(3, "", 4096)    = 0

[00007ff8d1b25600] write(1, "\33[H\33[2J  \33[4m 1 2 3 4 5 6 7 8 \33[0m\n", 35) = 35
[00007ff8d1b25600] write(1, "A |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "B |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "C |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "D |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "E |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "F |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "G |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "H |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "\n", 1)    = 1
[00007ff8d1b25600] write(1, "Rank: Seaman Recruit\n\n", 22) = 22
[00007ff8d1b25600] write(1, "Welcome to pewpewboat! We just loaded a pew pew map, start shootin'!\n", 69) = 69
[00007ff8d1b25600] write(1, "\n", 1)    = 1
[00007ff8d1b24f72] fstat(0, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 0), ...}) = 0
[00007ff8d1b25600] write(1, "Enter a coordinate: ", 20) = 20
[00007ff8d1b255a0] read(0, "H9\n", 1024) = 3

[00007ff8d1b25600] write(1, "\33[H\33[2J  \33[4m 1 2 3 4 5 6 7 8 \33[0m\n", 35) = 35
[00007ff8d1b25600] write(1, "A |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "B |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "C |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "D |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "E |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "F |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "G |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "H |_|_|_|_|_|_|_|_|\n", 20) = 20
[00007ff8d1b25600] write(1, "\n", 1)    = 1
[00007ff8d1b25600] write(1, "Rank: Seaman Recruit\n\n", 22) = 22
[00007ff8d1b25600] write(1, "You missed :(\n", 14) = 14
[00007ff8d1b25600] write(1, "\n", 1)    = 1
[00007ff8d1b25600] write(1, "Enter a coordinate: ", 20) = 20
[00007ff8d1b255a0] read(0, "01234567890123456789\n", 1024) = 21
[00007ff8d1b25600] write(1, "OjU\221\274\1r\377\334\255qQe\0054P\4\303\377\313i$\323\367MK\345^\217\2666\206G\24\221\355\221\207\2073r\222\33\33\343n\243\252\363I2\274\\O\v\306\252\200P\211\363!\370\245N\274\201\3479S\317\254\210VT\266\320\2105\201P\n", 82) = 82
[00007ff8d1b329e7] lseek(0, -5, SEEK_CUR) = -1 ESPIPE (Illegal seek)
[00007ff8d1b024c8] exit_group(1)        = ?
[????????????????] +++ exited with 1 +++
```

When we enter a long string it crashes (although it's reading 1024 bytes).

```
[00007ff8d1b255a0] read(0, "01234567890123456789\n", 1024) = 21
[00007ff8d1b25600] write(1, "OjU\221\274\1r\377\334\255qQe\0054P\4\303\377\313i$\323\367MK\345^\217\2666\206G\24\221\355\221\207\2073r\222\33\33\343n\243\252\363I2\274\\O\v\306\252\200P\211\363!\370\245N\274\201\3479S\317\254\210VT\266\320\2105\201P\n", 82) = 82
[00007ff8d1b329e7] lseek(0, -5, SEEK_CUR) = -1 ESPIPE (Illegal seek)
```

### ltrace
We can run ltrace to get some extra information.

```
root@kali:~/Desktop/pewpew# ltrace -iS -s9999 -o ltrace1.txt ./pewpewboat 
Loading first pew pew map...
```

ltrace options are similar. `-S` also traces system calls.

```
...
[0x400b09] __libc_start_main(0x403d86, 1, 0x7fffa84616d8, 0x403f10 <unfinished ...>
[0x403da7] time(0)                                                  = 1506201701
[0x403dae] srand(0x59c6d065, 0x7fffa84616d8, 0x7fffa84616e8, 0)     = 0
[0x403db8] malloc(576 <unfinished ...>
[0x7fb007f52b79] SYS_brk(0)                                         = 0xd47000
[0x7fb007f52b79] SYS_brk(0xd68000)                                  = 0xd68000
[0x403db8] <... malloc resumed> )                                   = 0xd47010
[0x403e4a] printf("%s", "Loading first pew pew map...\n" <unfinished ...>
[0x7fb007f4cf72] SYS_fstat(1, 0x7fffa8460e30)                       = 0
[0x7fb007f4d600] SYS_write(1, "Loading first pew pew map...\n", 29) = 29
[0x403e4a] <... printf resumed> )                                   = 29
[0x403d18] sprintf("loading... 0%", "loading... %d%%", 0)           = 13
[0x402cd8] memcpy(0x7fffa8461498, "loading... %d%%\0", 16)          = 0x7fffa8461498
[0x402d9d] memset(0x7fffa84614a9, '\0', 39)                         = 0x7fffa84614a9
[0x402fa2] memset(0x7fffa8461480, '\0', 152)                        = 0x7fffa8461480
...
```

And it keeps going on and on.

```
[0x403d18] sprintf("loading... 11032%", "loading... %d%%", 11032)   = 17
[0x402cd8] memcpy(0x7fffa8461498, "a1#\326X\375^f\037q\274\276g\266aP", 16) = 0x7fffa8461498
[0x402d9d] memset(0x7fffa84614a9, '\0', 39)                         = 0x7fffa84614a9
[0x402fa2] memset(0x7fffa8461480, '\0', 152)                        = 0x7fffa8461480
[0x403d18] sprintf("loading... 11033%", "loading... %d%%", 11033)   = 17
[0x402cd8] memcpy(0x7fffa8461498, "\035\a\312\364\034lf\244\316\357\356c\306\256\0\274", 16) = 0x7fffa8461498
[0x402d9d] memset(0x7fffa84614a9, '\0', 39)                         = 0x7fffa84614a9
[0x402fa2] memset(0x7fffa8461480, '\0', 152)                        = 0x7fffa8461480
```

So there might be some anti-debugging going on?

## Detour to function calls in x64

### Linux
Read these (trust me they are short reads):

- http://wiki.osdev.org/System_V_ABI
- http://wiki.osdev.org/Calling_Conventions - especially the cheatsheet.

In x86 function parameters were pushed to the stack from right to left before the `call`. Remember that return address is pushed to the stack right before call.

In x64 ABI (Application Binary Interface), we store the first 6 parameters in registers and the rest get pushed to the stack like x86. The registers are `rdi, rsi, rdx, rcx, r8, r9`.

For example if we call `randomfunc(p1, p2, p3, p4, p5, p6, p7, p8, p9)`:

- push p9
- push p8
- push p7
- mov  r9,  p6
- mov  r8,  p5
- mov  rcx, p4
- mov  rdx, p3
- mov  rsi, p2
- mov  rdi, p1

### Windows 
It's a bit different. 

Quick read: https://docs.microsoft.com/en-us/cpp/build/parameter-passing

"The first four integer arguments are passed in registers. Integer values are passed (in order left to right) in RCX, RDX, R8, and R9. Arguments five and higher are passed on the stack."

"Floating-point and double-precision arguments are passed in XMM0 - XMM3 (up to 4)."

More stuff: 

- https://docs.microsoft.com/en-us/cpp/build/calling-convention
- https://docs.microsoft.com/en-us/cpp/build/x64-software-conventions

## Remote debugging with IDA
Let's do some remote debugging because I don't ~~like~~ know GDB or r2.

Put a breakpoint on the `rand` at `0x0x403dae` which is actually at the start of `main`. (DAE ??? lololol eckss deee omg).

``` nasm
mov     rax, fs:28h      ; stack canary
mov     [rbp+var_8], rax
```

This part is similar to what we have seen in strace output.

time(0) - seed(time) - malloc(576 - 0x240)

Then printf("%s", "Loading first pew pew map...\n")

eax = 0 

### call sub_406C85
This is where loading happens.

sprintf("loading... 0%", "loading... %d%%", 0)


sub_402FA5


sub402B31("loading... %d%%")


67452301
EFCDAB89
98BADCFE
10325476

This is the MD5 initialization block.

0x1D in the end?


576 or 0x240 bytes from unk_6050E0[rax] are copied.


`sub_40304F(unk_6050E0, 0x240, 0x3B1EE5F6B3D99FF7)`

var18 = unk
var1C = 0x240
var28 = 0x3B1EE5F6B3D99FF7

called with var28

``` nasm
sub_403034 proc near

var_8= qword ptr -8

push    rbp
mov     rbp, rsp
mov     [rbp+var_8], rdi
mov     rax, [rbp+var_8]
imul    rax, 41C64E6Dh
add     rax, 3039h
pop     rbp
retn
```

unknown is xor-ed with result of sub_403034(0x3B1EE5F6B3D99FF7).

Prints the table: sub_403263

### Read Input
Probably should have come here in the first place.


``` nasm
.text:0000000000403806 mov     rdx, cs:stdin                   ; stream
.text:000000000040380D lea     rax, [rbp+s]
.text:0000000000403811 mov     esi, 11h                        ; n
.text:0000000000403816 mov     rdi, rax                        ; s
.text:0000000000403819 call    _fgets
```

Sub first coordinate from `0x41` (to get the index from `A`). Same thing happens with second but with `0x31` to get the index from `1`.

var40 = letter coordinate index from A (e.g. A=0 B=1 and so on).
var4C = number corrdinate index from 0 (e.g. 0=0 1=1 and so on)

``` nasm
cmp     [rbp+var_40], 0
js      short loc_4038B3
```

Check if coordinate from A is negative. `cmp` does a subtract and `js` jumps if sign flag is set. So if we entered something with a lower ASCII-HEX code than A (`0x41`) we jump to another place here.

``` nasm
cmp     [rbp+var_40], 7
jg      short loc_4038B3
```

Check if first coordinate over 7 (e.g. over `H`).

Same thing happens with second coordinate (the number).

var58 = 00 78 08 08 78 08 08 00 01 00 00 00 00 00 

-------

eax = first
edx = eax * 8 = first * 8

eax = second
eax = second + first * 8
edx = 1
ecx = second + first * 8
var38 = 1 shl cl = 1 shl (second + first * 8)

rax = var48 = 0008087808087800 = function param
rax = rax[8] = 01 (start from zero)

rdx = 01 or var38



var48 = 3B1EE5F6B3D99FF7 always


breakpoint at 

```
.text:0000000000403B57 mov     [rbp+var_30], 59h
.text:0000000000403B5B mov     [rbp+var_2F], 6Fh
.text:0000000000403B5F mov     [rbp+var_2E], 75h
```

### call    sub_403530(0008087808087800)
var_1A8 = 0008087808087800


```
mov     esi, 4
mov     rdi, rax
call    sub_402FA5
```

sub_402FA5("4 rand-ish digits", 4, 1)

MD5 initialization constants for variables


sub_402B31

```
[stack]:00007FFCC4A6F189 db  23h ; #
[stack]:00007FFCC4A6F18A db  45h ; E
[stack]:00007FFCC4A6F18B db  67h ; g
[stack]:00007FFCC4A6F18C db  89h ; ë
[stack]:00007FFCC4A6F18D db 0ABh ; ½
[stack]:00007FFCC4A6F18E db 0CDh ; -
[stack]:00007FFCC4A6F18F db 0EFh ; n
[stack]:00007FFCC4A6F190 db 0FEh ; ¦
[stack]:00007FFCC4A6F191 db 0DCh ; _
[stack]:00007FFCC4A6F192 db 0BAh ; ¦
[stack]:00007FFCC4A6F193 db  98h ; ÿ
[stack]:00007FFCC4A6F194 db  76h ; v
[stack]:00007FFCC4A6F195 db  54h ; T
[stack]:00007FFCC4A6F196 db  32h ; 2
[stack]:00007FFCC4A6F197 db  10h
```

Read new input

.text:00000000004036CE call    _fgets

.text:000000000040375E jz      short loc_403765

change to jmp

0000000000403C77

00000000004036CB 


F

b4 b5 b6 b7
c4
d4
e4 e5 e6 e7
f4
g4


H

b4 b8
c4 c8
d4 d8
e4 e5 e6 e7 e8
f4 f8
g4 g8


G

a2 a3 a4 a5 a6 a7
b1 b8
c1
d1
e1 e5 e6 e7 e8
f1 f8
g1 g8
h2 h3 h4 h5 h6 h7


U

d5 d8
e5 e8
f5 f8
g5 g8
h5 h6 h7 h8


Z

b4 b5 b6 b7 b8
c7
d6
e5
f4 f5 f6 f7 f8


R

a1 a2 a3
b1 b4
c1 c2 c3
d1 d3
e1 e4


E

d5 d6 d7
e5
f5 f6 f7
g5
h5 h6 h7


J

b2 b3 b4 b5 b6
c4
d4 
e4
f1 f4
g2 g3 


V

d3 d7
e3 e7
f3 f7
g4 g6
h5


O

d3 d4
e2 e5
f2 f5
g2 g5
h3 h4



```
Rank: Congratulation!

Aye!PEWYouPEWfoundPEWsomePEWlettersPEWdidPEWya?PEWToPEWfindPEWwhatPEWyou'rePEWlookingPEWfor,PEWyou'llPEWwantPEWtoPEWre-orderPEWthem:PEW9,PEW1,PEW2,PEW7,PEW3,PEW5,PEW6,PEW5,PEW8,PEW0,PEW2,PEW3,PEW5,PEW6,PEW1,PEW4.PEWNextPEWyouPEWletPEW13PEWROTPEWinPEWthePEWsea!PEWTHEPEWFINALPEWSECRETPEWCANPEWBEPEWFOUNDPEWWITHPEWONLYPEWTHEPEWUPPERPEWCASE.
Thanks for playing!
```

Replace `PEW` with space

```
Aye! You found some letters did ya? To find what you're looking for, you'll want to re-order them: 9, 1, 2, 7, 3, 5, 6, 5, 8, 0, 2, 3, 5, 6, 1, 4. Next you let 13 ROT in the sea! THE FINAL SECRET CAN BE FOUND WITH ONLY THE UPPER CASE.
```

We got letters

9, 1, 2, 7, 3, 5, 6, 5, 8, 0, 2, 3, 5, 6, 1, 4

0 1 2 3 4 5 6 7 8 9
F H G U Z R E J V O

O H G J U R E R V F G U R E H Z

BUTWHEREISTHERUM

Remember when we entered a long string, the binary returned some random shit?

Enter the secret and we get.

```
y0u__sUnK_mY__P3Wp3w_b04t@flare-on.com
```

It was in the damned thing that we found at the start!

-----------------

Try two
Choose `_fgets` in IDA. Select and highlight text `_fgets` and press X for references. We get two calls.

First one is for coordinates and second one is for entering the hash.


After entering a coordinate.

``` nasm
movzx   eax, [rbp+s]
and     eax, 0FFFFFFDFh
movsx   eax, al
sub     eax, 41h
mov     [rbp+first], eax
```

First char is changed to uppercase (lowercase - 0x20 = uppercase). If it's already uppercase nothing happens.

Subtract from 0x41 = offset from A.

``` nasm
movzx   eax, [rbp+var_2F]
movsx   eax, al
sub     eax, 31h
mov     [rbp+second], eax
```

Second char (number) from 0x31 (1) to get the offset.

Then checks if the offsets are in [0,7).

``` nasm
mov     eax, [rbp+first]
lea     edx, ds:0[rax*8]
mov     eax, [rbp+second]
add     eax, edx
```

eax = offset1 * 8 + offset2 (for example A0 = 0 - H8 = 63)

Essentially the coordinate is transformed to an index in the 64 cell array that represents the map (starting from 0).

The coordinates are written in memory just before the rank.

```
[heap]:00F7202C db  42h ; B
[heap]:00F7202D db  34h ; 4
[heap]:00F7202E db  53h ; S
[heap]:00F7202F db  65h ; e
[heap]:00F72030 db  61h ; a
[heap]:00F72031 db  6Dh ; m
[heap]:00F72032 db  61h ; a
[heap]:00F72033 db  6Eh ; n
[heap]:00F72034 db  20h
[heap]:00F72035 db  52h ; R
[heap]:00F72036 db  65h ; e
[heap]:00F72037 db  63h ; c
[heap]:00F72038 db  72h ; r
[heap]:00F72039 db  75h ; u
[heap]:00F7203A db  69h ; i
[heap]:00F7203B db  74h ; t
[heap]:00F7203C db    0
```

.text:0000000000403C73 add     [rbp+var_C], 0


ammo patch

.text:000000000040396F                 add     [rbp+var_4C], 1

-------------------

# 6 - payload.dll
Used x64dbg for this instead of IDA.

if edx == 1 

000007FEF55862 | E8 97 06 00 00        | call payload-olly.7FEF55868B8      |

## call payload-olly.7FEF55868B8

Anti-debugging?

000007FEF55868E4  | FF 15 96 97 00 00     | call qword ptr ds:[<&GetSystemTimeAsFileTime>]

rbp+10 = GetSystemTimeAsFileTime

https://msdn.microsoft.com/en-us/library/windows/desktop/ms724397(v=vs.85).aspx

**Rage Quit**

