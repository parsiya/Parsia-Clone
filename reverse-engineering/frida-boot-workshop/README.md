# Frida-Boot workshop
https://github.com/leonjza/frida-boot

Youtube link: https://www.youtube.com/watch?v=CLpW1tZCblo

# Chapter 1 - Part 1: LD_PRELOAD

```
~/code$ ldd pew
	linux-vdso.so.1 (0x00007ffd6abd4000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fd0396d2000)
	/lib64/ld-linux-x86-64.so.2 (0x00007fd0398a0000)
```

Identify shared libraries that we can mess with `LD_PRELOAD`.

If the binary is compiled statically == no external shared libraries.
`LD_PRELOAD` will not help here.

```
~/code$ gcc -static pew.c -o pew-static
~/code$ ldd pew-static 
	not a dynamic executable
```

**Not discussed in the video** but to discover shared library calls we can also
use `ltrace`.

```
~/code$ ltrace ./pew
puts("[+] Starting up!"[+] Starting up!                                         = 17
time(0)                                                                         = 1619288817
srand(0x608462f1, 0x55dd85dfc2a0, 0, 0x7ff07518e673)                            = 0
rand(1, 5, 0x7ff07525c1d0, 0)                                                   = 0x1340f51f
printf("[+] Sleeping for %d seconds\n", 5[+] Sleeping for 5 seconds             = 27
sleep(5)                                                                        = 0
rand(1, 5, 0, 0x7ff07516ae93)                                                   = 0xaf08cb7
printf("[+] Sleeping for %d seconds\n", 4[+] Sleeping for 4 seconds)            = 27
sleep(4)                                                                        = 0
rand(1, 5, 0, 0x7ff07516ae93)                                                   = 0x61534c8c
printf("[+] Sleeping for %d seconds\n", 2[+] Sleeping for 2 seconds             = 27
sleep(2^C <no return ...>
--- SIGINT (Interrupt) ---
+++ killed by SIGINT +++
```

Or use `nm`:

```
~/code$ nm -D pew
    w __cxa_finalize@@GLIBC_2.2.5
    w __gmon_start__
    w _ITM_deregisterTMCloneTable
    w _ITM_registerTMCloneTable
    U __libc_start_main@@GLIBC_2.2.5
    U printf@@GLIBC_2.2.5
    U puts@@GLIBC_2.2.5
    U rand@@GLIBC_2.2.5
    U sleep@@GLIBC_2.2.5
    U srand@@GLIBC_2.2.5
    U time@@GLIBC_2.2.5
```

We want to hook `sleep` and ``.

Make our own implementation of sleep. We need to know the function signature.

```c
#include <stdio.h>

unsigned int sleep(unsigned int seconds) {
    
    printf(" [-] sleep goes brrr\n");
    return 0;
}
```

Now, we need to compile it into a shared object with `gcc` using `-shared`.
`fPIC` generates position-independent code.

```
~/code$ gcc -fPIC -shared ../software/fake_sleep.c -o fake_sleep.so
```

`LD_PRELOAD` needs a full path.

```
~/code$ LD_PRELOAD=./fake_sleep.so ./pew
```

The app prints the strings but does not sleep at all because we have modified
the `sleep` function.

Now let's make a proxy so. E.g., `fake_sleep` calls `sleep`. To get the original
sleep we need to call [dlsym][dlsym-man].

[dlsym-man]: https://man7.org/linux/man-pages/man3/dlsym.3.html

```cpp
#define _GNU_SOURCE

#include <stdio.h>
#include <dlfcn.h>

// man 3 sleep
//  unsigned int sleep(unsigned int seconds);
unsigned int sleep(unsigned int seconds) {

    // you've never slept this well in your life!
    printf("[-] sleep goes brrr\n");

    seconds = 1;

    unsigned int (*original_sleep)(unsigned int);
    // "RTLD_NEXT": Get the handle for the next symbol named "sleep"
    original_sleep = dlsym(RTLD_NEXT, "sleep");

    return (original_sleep)(seconds);
}
```

Now, we need to add the `-ldl` switch **in the end**.

`LD_PRELOAD=./fake_sleep.so ./pew`: each sleep is now 1 second.

----------

# Chapter 1 - Part 2: gdb
`gdb -q ./pew`

Inside we can do `info func` to list all functions. Some functions have plt in
the end `printf@plt`. `PLT` stands for Procedure Linkage Table. Inside PLT we
have `GOT` or Global Offset Table.

1. First call: Check if `printf` exists in the GOT. It's not because it has not
   been called before.
2. If it does not exist, dynamic linker it looks for it in all of the shared
   libraries.
3. Write the record in the GOT and store the address of the real `printf`.
4. Every new call, the program uses the record in the GOT.

Inside gdb (probably need `gef`) we can do `got` to see the GOT. The items that have been resolved are
in green and the rest are red (color is definitely `gef`).

```
gef➤  got

GOT protection: Partial RelRO | GOT functions: 6
 
[0x5569a25ec018] puts@GLIBC_2.2.5  →  0x7f9b8a61b030    # this is green
[0x5569a25ec020] printf@GLIBC_2.2.5  →  0x5569a25e9046  # the rest is yellow
[0x5569a25ec028] srand@GLIBC_2.2.5  →  0x5569a25e9056
[0x5569a25ec030] time@GLIBC_2.2.5  →  0x5569a25e9066
[0x5569a25ec038] sleep@GLIBC_2.2.5  →  0x5569a25e9076
[0x5569a25ec040] rand@GLIBC_2.2.5  →  0x5569a25e9086

gef➤  info symbol 0x5569a25ec018
puts@got.plt in section .got.plt of /root/code/pew # puts have been resolved to its actual address

gef➤  info symbol 0x5569a25ec020
printf@got.plt in section .got.plt of /root/code/pew # printf has not been resolved, yet
```

**Rage quit, moved on to the Frida stuff.**

----------

# Chapter 2 - Part 1: Frida

## Some tmux Stuff
Everything starts with `ctrl+b` then you get one character to do stuff.

`ctrl+b` then `w` list all windows.

To destroy any window, select it from the list above, then `ctrl+b` then `&`. A prompt will ask for `y/n`, press `y`.

splits: `ctrl+b` then

* `%`: horizontal split
* `"`: vertical split

```
ctrl+b then
o  swap panes
q  show pane numbers
x  kill pane
space - toggle between layouts
```

From outside to kill and list sessions.

```
tmux list-session

# then kill
tmux kill-session -t 2
```

scroll up and down

`ctrl+b` `[` then you can use `page up/down` or `arrow key`. `ctrl+c` when done.

tmux cheat sheet: https://gist.github.com/MohamedAlaa/2961058

## Frida REPL
`frida pew --runtime=v8` will attach to the process named `pew`. Will not work
if we have multiple processes named `pew`. We can do `frida -p pid` instead.

Using the v8 runtime allows us to use things like arrow functions or raw format
strings (e.g., `value is ${val}`).

`frida pew -l index.js` loads the script. We can modify the script on the fly
and after the save the script will be executed again.

# Chapter 2 - Part 2: Interceptor
https://frida.re/docs/javascript-api/#interceptor

The target in the end is a memory address. In practice it can be offset or
symbol. With symbol we get the address quickly.

## Resolving sleep in gdb
Let's try to resolve `sleep` in pew.

```
~/code$ nm pew | grep -i "sleep"
    U sleep@@GLIBC_2.2.5
```

Next, we need to figure out which library has libc.

```
~/code$ ldd pew
    linux-vdso.so.1 (0x00007fff4e3de000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f140beac000)
    /lib64/ld-linux-x86-64.so.2 (0x00007f140c07a000)
```

To see the address of `sleep` inside libc.

```
# -D or -dynamic
# Display the dynamic symbols rather than the normal symbols. This is only
# meaningful for dynamic objects, such as certain types of shared libraries.

~/code$ nm -D /lib/x86_64-linux-gnu/libc.so.6 | grep -i "sleep"
000000000010a3c0 T __clock_nanosleep@@GLIBC_PRIVATE
000000000010a3c0 W clock_nanosleep@@GLIBC_2.17
00000000000cae80 T __nanosleep@@GLIBC_2.2.6
00000000000cae80 W nanosleep@@GLIBC_2.2.5
00000000000f35d0 T __nanosleep_nocancel@@GLIBC_PRIVATE
00000000000cad90 W sleep@@GLIBC_2.2.5
0000000000084d70 T thrd_sleep@@GLIBC_2.28
00000000000f5870 T usleep@@GLIBC_2.2.5
```

So the offset of `sleep` is `0xcad90` here.

To confirm it:

1. Run pew in gdb.
2. `b *main` and then run with `r`.
3. `info proc map` or `vmmap` to get the libc's 0x00 offset address to get its base address.
4. Add `0xcad90` to it to get the `sleep`'s address.

```
gef➤  info proc map
process 411
Mapped address spaces:

        Start Addr           End Addr       Size     Offset objfile
    0x55b349b21000     0x55b349b22000     0x1000        0x0 /root/code/pew
    0x55b349b22000     0x55b349b23000     0x1000     0x1000 /root/code/pew
    0x55b349b23000     0x55b349b24000     0x1000     0x2000 /root/code/pew
    0x55b349b24000     0x55b349b25000     0x1000     0x2000 /root/code/pew
    0x55b349b25000     0x55b349b26000     0x1000     0x3000 /root/code/pew
    0x7fdd58148000     0x7fdd5816d000    0x25000        0x0 /lib/x86_64-linux-gnu/libc-2.30.so # this is what we want, offset 0x00
    0x7fdd5816d000     0x7fdd582b7000   0x14a000    0x25000 /lib/x86_64-linux-gnu/libc-2.30.so
    0x7fdd582b7000     0x7fdd58301000    0x4a000   0x16f000 /lib/x86_64-linux-gnu/libc-2.30.so
    0x7fdd58301000     0x7fdd58304000     0x3000   0x1b8000 /lib/x86_64-linux-gnu/libc-2.30.so
    0x7fdd58304000     0x7fdd58307000     0x3000   0x1bb000 /lib/x86_64-linux-gnu/libc-2.30.so
    ...

gef➤  vmmap
[ Legend:  Code | Heap | Stack ]
Start              End                Offset             Perm Path
0x000055b349b21000 0x000055b349b22000 0x0000000000000000 r-- /root/code/pew
0x000055b349b22000 0x000055b349b23000 0x0000000000001000 r-x /root/code/pew
0x000055b349b23000 0x000055b349b24000 0x0000000000002000 r-- /root/code/pew
0x000055b349b24000 0x000055b349b25000 0x0000000000002000 r-- /root/code/pew
0x000055b349b25000 0x000055b349b26000 0x0000000000003000 rw- /root/code/pew
0x00007fdd58148000 0x00007fdd5816d000 0x0000000000000000 r-- /lib/x86_64-linux-gnu/libc-2.30.so # offset 0x00 (3rd column)
0x00007fdd5816d000 0x00007fdd582b7000 0x0000000000025000 r-x /lib/x86_64-linux-gnu/libc-2.30.so
0x00007fdd582b7000 0x00007fdd58301000 0x000000000016f000 r-- /lib/x86_64-linux-gnu/libc-2.30.so
0x00007fdd58301000 0x00007fdd58304000 0x00000000001b8000 r-- /lib/x86_64-linux-gnu/libc-2.30.so
0x00007fdd58304000 0x00007fdd58307000 0x00000000001bb000 rw- /lib/x86_64-linux-gnu/libc-2.30.so
```

The address is `0x7fdd58148000` in both commands. So `sleep` will be
`7fdd58148000 + cad90` = `7fdd58212d90` (we do need to do this manually).

We can check it in gdb:

```
gef➤  info symbol 0x7fdd58148000 + 0xcad90
sleep in section .text of /lib/x86_64-linux-gnu/libc.so.6
```

## Resolving sleep in Frida
We can get the base address in different ways:

* `Process.enumerateModulesSync`
* `Module.getBaseAddress`
* `Process.getModuleByName.enumerateExports`
* `Module.getExportByName`
* `DebugSymbol.getFunctionByName`

### Process.enumerateModulesSync

```
[Local::pew]-> Process.enumerateModulesSync();

    // ...
    {
        "base": "0x7f28c98c6000",
        "name": "libc-2.30.so",
        "path": "/lib/x86_64-linux-gnu/libc-2.30.so",
        "size": 1830912
    },
```

But we can also pass a filter here which is a function.

```js
Process.enumerateModulesSync().filter(ex => ex.name.includes("libc"));

// Without the v8 runtime, we had to use:

Process.enumerateModulesSync().filter(function(m) { return m.name.includes("libc");});
```

Both return the same result:

```json
[
    {
        "base": "0x7f7286eb2000",
        "name": "libc-2.30.so",
        "path": "/lib/x86_64-linux-gnu/libc-2.30.so",
        "size": 1830912
    }
]
```

We can also do

```js
[Local::pew]-> Process.getModuleByName("libc-2.30.so");
{
    "base": "0x7f7286eb2000",
    "name": "libc-2.30.so",
    "path": "/lib/x86_64-linux-gnu/libc-2.30.so",
    "size": 1830912
}
```

We can just get the `base` with `.base` in both cases:

```js
[Local::pew]-> Process.getModuleByName("libc-2.30.so").base;
"0x7f7286eb2000"
// enumerateModulesSync returns an array so we need to choose the first element.
[Local::pew]-> Process.enumerateModulesSync().filter(ex => ex.name.includes("libc"))[0].base;
"0x7f7286eb2000"
```

### Module.getBaseAddress

```js
[Local::pew]-> Module.getBaseAddress("libc-2.30.so");
"0x7f7286eb2000"
```

Response is a native pointer so we can `add` to directly get the `sleep`
offset.

```js
[Local::pew]-> Module.getBaseAddress("libc-2.30.so").add("0xcad90");
"0x7f7286f7cd90"
```

### Process.getModuleByName.enumerateExports
`sleep` is an export in libc so we can just ask Frida to resolve it for us.

```js
[Local::pew]-> Process.getModuleByName("libc-2.30.so").enumerateExports().filter(ex => ex.name === "sleep");
[
    {
        "address": "0x7f7286f7cd90",
        "name": "sleep",
        "type": "function"
    }
]
```

It's an array so you should get the address with `[0].address` (append to the
end of the command above).

### Module.getExportByName

```js
[Local::pew]-> Module.getExportByName(null, "sleep");
"0x7f7286f7cd90"

// first argument is the name of the library but sleep is unique so we do not
// care about duplicates

[Local::pew]-> Module.getExportByName("libc-2.30.so", "sleep");
"0x7f7286f7cd90"
```
 
### DebugSymbol.getFunctionByName

```js
[Local::pew]->  DebugSymbol.getFunctionByName("sleep")
"0x7f7286f7cd90"
```

## Interceptor
`Inteceptor.attach(target, callbacks[, data]);`

callbacks is an object with two functions.

```js
Interceptor.attach(sleepPtr, {

    onEnter: function(args) {},  // we can modify the arguments

    onLeave: function(retval) {} // we can modify the return value
});
```

**Note:** It's important to not use the arrow function syntax for `onEnter` and
`onLeave`. Oh, well!

Now, we can modify the `sleep` function with Frida. I am going to use ES6
because I will change my runtime to v8.

```js
// frida pew -l myinterceptor-attach.js --runtime=v8

var sleep = Module.getExportByName(null, "sleep");

Interceptor.attach(sleep, {
    // in this case using the arrow function is not that bad because we are not
    // doing anything complex.

    onEnter: args => { console.log("[*] Sleep from Frida!"); },

    onLeave: retval => {console.log("[*] Done sleeping from Frida!"); }
});
```

# Chapter 2 - Part 3: Hooking Arguments and Return Values

## Modifying Arguments
We can modify the arguments inside `onEnter`.

* `args` does not know how many arguments are in there.
* `args[0]` is the first arg.
* Args are of type [NativePointer][nativepointer-docs].

[nativepointer-docs]: https://frida.re/docs/javascript-api/#nativepointer

Frida does not do bounds checking here. It's possible to read the memory past
the valid arguments. E.g., `args[10]` when the function only has 2 arguments.

```js
// parse-sleep-args.js
var sleep = Module.getExportByName(null, "sleep");

Interceptor.attach(sleep, {

    onEnter: args => { console.log("[*] Argument for sleep() => ", parseInt(args[0])); },

    onLeave: retval => { console.log("[*] Done sleeping from Frida!"); }
});
```

Now, we can modify the arguments. Create a new pointer and assign it.

```js
args[0] = ptr("0x01");
args[0] = new NativePointer("0x01");
```

Let's modify sleep argument to 2.

```js
// modify-sleep-args.js
var sleep = Module.getExportByName(null, "sleep");

Interceptor.attach(sleep, {

    onEnter: args => {

        console.log("[*] The original argument for sleep() => ", parseInt(args[0]));
        args[0] = ptr("0x02"); // change it to 2
    },

    onLeave: retval => { console.log("[*] Done sleeping from Frida!"); }
});
```

#### How to Allocate Strings
Allocate a new char array with `Memory.allocUtf8String` like this:

```js
onEnter: function (args) {
    var buf = Memory.allocUtf8String('mystring'); // create a new string on memory
    this.buf = buf;                               // assign it to this
    args[0] = buf;                                // pass it to args
}
```

According to
[Best Practices - String allocation][frida-best-practices-string-allocation]

> this is bound to an object that is per-thread and per-invocation, and anything
> you store there will be available in onLeave, and this even works in case of
> recursion. This way you can read arguments in onEnter and access them later in
> onLeave. It is also the recommended way to keep memory allocations alive for
> the duration of the function-call.

[frida-best-practices-string-allocation]: https://frida.re/docs/best-practices/#string-allocation-utf-8utf-16ansi

Let's modify `printf` arguments.

```js
var sleep = Module.getExportByName(null, "printf");
var strBuf = Memory.allocUtf8String("pewpewpew\n");

Interceptor.attach(sleep, {

    onEnter: args => {
        // this did not work, I would get the pews printed after detaching Frida
        // maybe because I am in an arrow function?
        // var strBuf = Memory.allocUtf8String("pewpewpew\n"); 

        console.log("[*] The original argument for printf() => ", args[0]);
        args[0] = strBuf;
    }

    // onLeave: retval => { console.log("[*] Done sleeping from Frida!"); }
});
```

#### Get Registers/Context
`this` does not work in the arrow function so, we have to use a normal one.

```js
// get-context.js
var sleep = Module.getExportByName(null, "printf");

Interceptor.attach(sleep, {

    onEnter: function(args) {
        console.log(JSON.stringify(this.context, null, 4));
    }
});
```

We can modify the registers here, too.

## Modifying Return Values
Trying to modifying the return value `rand_range` in pew. We need to do
`retval.replace(ptr(...));`.

```js
// modify-return-rand-range.js
var randRange = DebugSymbol.getFunctionByName("rand_range"); // we have symbols

Interceptor.attach(randRange, {

    onLeave: retval => { retval.replace(ptr("0x01")); }
});
```

Without using arrow functions and like it was mentioned in the string allocation
section, we can pass variables to `this` inside `onEnter` and then use them in
`onLeave`.

```js
// modify-return-rand-range2.js
var randRange = DebugSymbol.getFunctionByName("rand_range"); // we have symbols

Interceptor.attach(randRange, {

    onEnter: function(args) {
        this.arg0 = args[0];
    },

    onLeave: function(retval) {
        console.log(retval);
        retval.replace(this.arg0); // now we can use this.arg0 here
    }
});
```

# Chapter 2 - Part 4: Reusing Existing Code
The `crypt` utility asks for a PIN and then checks it with `test_pin`. We want
to hook this function and return 1.

[hexdump][hexdump] generates a hex dump from an ArrayBuffer or NativePointer.

[hexdump]: https://frida.re/docs/javascript-api/#hexdump

```js
var testPIN = DebugSymbol.getFunctionByName("test_pin");

Interceptor.attach(testPIN, {

    onEnter: function(args) {
        console.log("test_pin args:", hexdump(args[0]));
    },

    onLeave: function(retval) {
        console.log("test_pin return value:", retval);
    }
});
```

Let's modify the return value to always return `1`.

```js
var testPIN = DebugSymbol.getFunctionByName("test_pin");

Interceptor.attach(testPIN, {

    onEnter: function(args) {
        // console.log("test_pin args:", hexdump(args[0]));
    },

    onLeave: function(retval) {
        // console.log("test_pin return value:", retval);
        retval.replace(ptr("0x01"));
    }
});
```

## Calling Functions
Try and call `test_pin` manually. We use [NativeFunction][nativefunction].
Create a JavaScript wrapper around a function. We can use it to call the target
function.

[nativefunction]: https://frida.re/docs/javascript-api/#nativefunction

`NativeFunction(address, returnType, argTypes[, abi])`

```js
var testPIN = DebugSymbol.getFunctionByName("test_pin");
// Wrapper. output is int and input is an array with one pointer.
var testPINFunction = new NativeFunction(testPIN, "int", ["pointer"]);

var pin = Memory.allocUtf8String("1234");
var res = testPINFunction(pin);
console.log("test_pin(1234):", res);
```

We can do this to call arbitrary functions or do things like bruteforce. Run
with `--runtime=v8` to enable the raw string.

```js
// frida crypt -l crypt-bruteforce-pin.js  --runtime=v8

var testPIN = DebugSymbol.getFunctionByName("test_pin");
// Wrapper. output is int and input is an array with one pointer.
var testPINFunction = new NativeFunction(testPIN, "int", ["pointer"]);

for (var i=0; i<9999; i++) {
    var pin = Memory.allocUtf8String(i);
    var res = testPINFunction(pin);
    console.log(`test_pin(${i}) = ${res}`);

    if (res === 1) {
        console.log("Found PIN:", pin);
        break;
    }
}
```

----------
# Chapter 3 - Part 1: Python Tools
We can use our own Python tools and use the message bus to pass info between the
agent and the Python script. Do fancy stuff.

```py
import frida
import sys

session = frida.attach("crypt") # attach to crypt
script = session.create_script("""
    console.log(Frida.version);
""")
script.load()
```

If we want to load an external agent instead.

```js
// tool2.js
console.log(Frida.version);
```

```py
import frida
import sys

with open("tool2.js", "r") as f:
    agent = f.read()

session = frida.attach("crypt")
script = session.create_script(agent, runtime="v8")
script.load()
```

# Chapter 3 - Part 2: Send and Receive
`script.load()` usually has a maximum time of 30 seconds. You don't want a lot
of stuff happening in the initial script that is loaded.

## Send From JavaScript
In Python and JavaScript we can send message with [send][send]:
`send(message[,data])`.

[send]: https://frida.re/docs/javascript-api/#communication-send
[recv]: https://frida.re/docs/javascript-api/communication-recv

To [receive][recv] messages in Python, we need to create handlers:

```python
# tool4.py
import frida
import sys

# define the handler
def incoming(message, data):
    print(message)
    print(data)

with open("tool4.js", "r") as f:
    agent = f.read()

session = frida.attach("crypt")
script = session.create_script(agent, runtime="v8")
script.on("message", incoming)
script.load()
```

The agent is the same, it sends out the PIN instead of printing it locally:

```js
// tool4.js
var testPIN = DebugSymbol.getFunctionByName("test_pin");
// Wrapper. output is int and input is an array with one pointer.
var testPINFunction = new NativeFunction(testPIN, "int", ["pointer"]);

send("Starting brute forcer");

for (var i=0; i<9999; i++) {
    var pin = Memory.allocUtf8String(i.toString());
    var res = testPINFunction(pin);

    if (res === 1) {
        send(`Found PIN: ${i}`);
        send("Finished brute forcing");
        break;
    }
}
```

And the result is the same:

```
~/code$ python3 tool4.py 
{'type': 'send', 'payload': 'Starting brute forcer'}
{'type': 'send', 'payload': 'Found PIN: 3428'}
{'type': 'send', 'payload': 'Finished brute forcing'}
```

## Send From Python
Inside Python we can do:

```py
script.post("whatever")
sys.stdin.read() # wait for input to see the output from the script
```

And in JavaScript we have a `recv` function:

```js
recv(function(msg) {
    console.log("message:" + msg);
});

// recv(msg => console.log("message:", msg);)
```

## Frida RPC Interface
Exports functions in the agent and add them to `rpc.exports` and in the Python
script use them with `script.exports.func`.

https://frida.re/docs/javascript-api/#rpc-exports

Function names in JavaScript vs. Python? The talk says `testPin` in JS becomes
`test_pin` in Python. How is the conversion done? Can I find any
documentation/articles about this?

Apparently, this is to keep PEP8 in the Python side.

> I should add that the intention here is to be able to follow the
> camelCase-convention commonly used in the JavaScript world – and used by
> Frida's own APIs – and still be able to follow PEP 8 on the Python side, i.e.
> `readByte` on the JS side becomes `read_byte` on the Python side. Similarly a
> C#/.NET binding would map it to `ReadByte`. Cheers!

https://github.com/frida/frida-python/issues/104#issuecomment-281666759

**Tip:** Better to export everything as all lower case.

Seems like we can also name things in `rpc.exports` like this:

```js
function internalFunction(e) {
    // ...
}

rpc.exports = {
    // export an internal function
    exportedName: internalFunction, // exported_name in Python
    // we can also define and export a function right here
    name2: function(e) {
        // ...
    }
}
```

### Refactor Bruteforce
The agent is like this:

```js
// tool6.js
var testPIN = DebugSymbol.getFunctionByName("test_pin");
// Wrapper. output is int and input is an array with one pointer.
var testPINFunction = new NativeFunction(testPIN, "int", ["pointer"]);

function brute() {
    send("Starting brute forcer");

    for (var i=0; i<9999; i++) {
        var pin = Memory.allocUtf8String(i.toString());
        var res = testPINFunction(pin);

        if (res === 1) {
            send(`Found PIN: ${i}`);
            send("Finished brute forcing");
            break;
        }
    }
};

rpc.exports = {
    bruteForcer: brute // become brute_forcer in Python
};
```

We can call it as `brute_forcer` in Python:

```py
# tool6.py
import frida
import sys

# define the handler
def incoming(message, data):
    print(message)

with open("tool6.js", "r") as f:
    agent = f.read()

session = frida.attach("crypt")
script = session.create_script(agent, runtime="v8")
script.on("message", incoming)
script.load()
api = script.exports
api.brute_forcer()
sys.stdin.read()
```

### Bruteforce in Python
Change the agent and export the `test_pin` function, then loop and brute force
in Python. The agent just exports the `testpin` function.

```js
// tool7.js
var testPIN = DebugSymbol.getFunctionByName("test_pin");
// Wrapper. output is int and input is an array with one pointer.
var testPINFunction = new NativeFunction(testPIN, "int", ["pointer"]);

function testPin(e) {
    var pin = Memory.allocUtf8String(e.toString());
    return testPINFunction(pin);
}

rpc.exports = {
    testpin: testPin // all lowercase export name
};
```

And the Python script calls `testpin` and does the bruteforce.

```py
# tool7.py
import frida
import sys

with open("tool7.js", "r") as f:
    agent = f.read()

session = frida.attach("crypt")
script = session.create_script(agent, runtime="v8")
script.load()
api = script.exports

# we can do the loop here
for pin in range(0, 9999):
    if(api.testpin(pin) == 1): # we are converting it to string in the JS
        print(f"Pin found: {pin}")
        break
```

# Chapter 3 - Part 3: Typescript
We are gonna use https://github.com/oleavr/frida-agent-example.

Rewriting `testPIN` in TypeScript.

```ts
// agent1.ts
// reimplementing testPIN in Typescript
import { log } from "./logger";

const testPINSymbol = DebugSymbol.getFunctionByName("test_pin");
const testPINFunction = new NativeFunction(testPINSymbol, "int", ["pointer"]);

function testPIN(pin: string) {
    const pinStr = Memory.allocUtf8String(pin);
    return testPINFunction(pinStr);
};

rpc.exports = {
    testpin: testPIN
};
```

And the Python tool does not change other than loading `_agent.js`.

## Inject a Web Server into the Target Process
We need to modify our agent and do it.

```js
// agent2.ts
import { log } from "./logger";
import * as http from "http";

const testPINSymbol = DebugSymbol.getFunctionByName("test_pin");
const testPINFunction = new NativeFunction(testPINSymbol, "int", ["pointer"]);

function testpin(p: string) {
    const pin = Memory.allocUtf8String(p);
    return testPINFunction(pin);
};

function httpServer() {
    http.createServer((req, res) => {
        const pin = req.url? req.url.replace('/', '') : '';
        const check = testpin(pin);

        log(`Request to check ${req.url} returned ${check}`);

        if (check == 1) {
            res.writeHead(200, {'Content-Type': 'text/plain'});
            res.write(`Welcome!\n`);
        } else {
            res.writeHead(401, {'Content-Type': 'text/plain'});
            res.write(`Wrong PIN\n`);
        }

        res.end();
    }).listen(1337);
};


rpc.exports = {
    testpin: testpin,
    httpServer: httpServer
}
```

And the Python tool is still similar:

```python
# tool2.py
import frida
import sys

with open("_agent.js", "r") as f:
    agent = f.read()

session = frida.attach("crypt")
script = session.create_script(agent)
script.load()

api = script.exports
print("starting HTTP server...")
api.httpserver()

# keep the server alive now
sys.stdin.read()

```

Now, we can query `http://localhost:1337/1234` to test if PIN is 1234.
`curl http://localhost:1337/3428`.

# Chapter 3 - Part 4: frida-tools

`frida-trace crypt -i "ato*"` generates handlers to log/hook (?) for these
functions.

# Chapter 4 - Part 5: Operating Modes
`frida-server` is the most important one. Run it on the device and connect to
it, similar to IDA server.

`frida-gadget` inject into the app or embed it into the app. See
https://koz.io/using-frida-on-android-without-root/.
