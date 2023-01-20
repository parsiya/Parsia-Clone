---
draft: false
toc: false
comments: false
categories:
- Development
title: "Go"
wip: false
snippet: "Go notes - copied from my website at [https://parsiya.net/go/](https://parsiya.net/go/)"
---

**Note: You can use these notes instead, but it's nice to have everything in one page:**

- [https://github.com/parsiya/Hacking-with-Go](https://github.com/parsiya/Hacking-with-Go)
- [Gophercises - Lessons Learned](https://parsiya.net/blog/2018-10-06-gophercises-lessons-learned/) 

These are my notes when learning go from the [Tour of Go](https://tour.golang.org/)
and some other sources. A lot of copy/pasted from them and I have used
double-quotes to indicate those are not written by me to the best of my ability.
This is not something original and is mostly here as a quick lookup reference
while learning Go. I will update this as I learn more.

# Packages, variables, and functions

## Exported names
In Go, a name is exported if it begins with a capital letter.

When importing a package, you can refer only to its exported names. Any
`unexported` names are not accessible from outside the package.

## Functions
Unlike C, type comes after variable name except pointers.

Last `int` is function return type (obviously).

``` go
func add(x int, y int) int {
	return x + y
}
```

Then use it normally

``` go
fmt.Println(add(10,20))
```

## Multiple results
A function can return any number of results. Gone are the days when we had to
use pointers in function parameters as extra return values.

``` go
package main

import "fmt"

func addTwo1(x int, y int) (int, int) {
	return x+2, y+2
}

func main() {
	fmt.Println(addTwo1(10,20))
}
```

## Named return values
Go's return values may be named. If so, they are treated as variables defined at
the top of the function.

A return statement without arguments returns the named return values. This is
known as a "naked" return. _Don't use them._

``` go
package main

import "fmt"

func addTwo2(x int, y int) (xPlusTwo int, yPlusTwo int) {
	xPlusTwo = x + 2
	yPlusTwo = y + 2

	// Could do naked return too
	return xPlusTwo, yPlusTwo
}

func main() {
	fmt.Println(addTwo2(20,30))
}
```

## Variables
Use `var`.

`var x int`

Can be combined:

`var x,y int` == `var x int, y int`. Similar to C when we had `int x,y;`.

### Initialize:

`var a, b int = 10, 20` == `var a int = 10` and `var b int = 20`.

If initializer is there then the type can be omitted like scripting languages
(e.g. Python):

`var sampleInt, sampleBoolean, sampleString = 30, true, "Hello"`

``` go
package main

import "fmt"

func main() {
	var a, b int = 10, 20
	var sampleInt, sampleBoolean, sampleString = 30, true, "Hello"

	fmt.Println(a, b , sampleInt, sampleBoolean, sampleString)
}
```

If no initial value is assigned to a declared variable, it will get a `zero`
value:

* 0 for numeric types (int, float, etc.)
* false for the boolean type
* "" (the empty string) for strings

### Short variable declarations
Inside a function, the `:=` short assignment statement can be used in place of a
`var` declaration with implicit type.

Outside a function, every statement begins with a keyword (`var`, `func`, and so
on) and so the `:=` construct is not available.

``` go
package main

import "fmt"

func main() {
	sampleInt, sampleBoolean, sampleString := 30, true, "Hello"

	fmt.Println(sampleInt, sampleBoolean, sampleString)
}
```

We can also put `var` statements in different lines (increases readability):

``` go
var (
	sampleInt			= 30
	sampleBoolean		= true
	sampleString 		= "Hello"
)
```

## Basic types

``` go
bool

string

int  int8  int16  int32  int64	// use int unless you want a specific size
uint uint8 uint16 uint32 uint64 uintptr	// same here, use uint

byte // alias for uint8

rune // alias for int32
     // represents a Unicode code point

float32 float64

complex64 complex128
```

## Casting
Casting needs to be explicit, unlike C where some castings worked out of the box.

For example one of my favorites in C was to make a division but put the result
in an `int` to skip the remainder.

Casting in Go is like this: `float32(whatever)`

``` go
package main

import (
	"fmt"
)

func main() {
	var a, b int = 20, 30
	// Need to convert a and b to float32 before the division
	var div float32 = float32(a)/float32(b)
	var divInt = int(div)
	fmt.Println(div, divInt)
}
```

`%T` is the print ~~switch~~ verb to print type of a variable. For example
`fmt.Printf("v is of type %T\n", v)`.

## Constants
Declared with `const` keyword. Can be character, string, boolean or numeric.
Cannot use `:=`. Make the first character capital for constants (coding
standard?).

``` go
package main

import "fmt"

const Whatever = "whatever"

func main() {
	fmt.Println(Whatever)

	const One = 1
	fmt.Println(One)
}
```

# Flow control statements: for, if, else, switch and defer

## For
Similar to C with two differences:

* No parenthesis around the three components. Having parenthesis will give you
  an error (*sigh*) when you are using the three components separated by
  semicolons.
* Curly braces `{ }` are always required and the first one needs to be in the
  same line as for, if, etc.

``` go
sum := 0
for i :=0; i <20; i++ {
	sum += i
}
```

Init and post (first and last) components are optional.

``` go
i := 0
for ; i <20; {
	i++
}
```

Without the semicolons, it will be a `while` (*why not just have a while?*).

``` go
i := 0
for i <20 { // while (i<20)
	i++
}
```

Without the condition it will loop forever or `while(1)`.

``` go
for {	// while(1)
	...
}
```

From `Effective Go` a better C/Golang comparison:

``` go
// Like a C for
for init; condition; post { }

// Like a C while
for condition { }

// Like a C for(;;)
for { }
```

## if
Does not need parenthesis (although you still can use them if you do not have a
init component which is separated from the condition with a semicolon) but needs
curly braces.

> Like for, the if statement can start with a short statement to execute before
> the condition.
> 
> Variables declared by the statement are only in scope until the
> end of the if."

``` go
package main

import "fmt"

func main() {
	if whatever := 20; whatever > 10 {
		fmt.Println("Inside if:", whatever)
	}
	// Cannot use the variable whatever here
}
```

## else
`else` is similar to C else.

> Variables declared inside an if short statement are also available inside any
> of the else blocks.

``` go
package main

import "fmt"

func main() {

	if whatever := 20; whatever > 100 {
		fmt.Println("Inside if:", whatever)
	} else {
		// Can use whatever here
		fmt.Println("Inside else:", whatever)
	}
	// Cannot use whatever here
}
```

## switch
Similar to C switch with some differences:

* Doesn't automatically go to the next `switch` statement unless you have
  `fallthough` at the end. "The `fallthrough` must be the last thing in the
  case."
* Can have a short statement similar to if (the statement before the case that
  gets executed).

``` go
// Code taken from the tour
package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Print("Go runs on ")
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("OS X.")
	case "linux":
		fmt.Println("Linux.")
	default:
		// freebsd, openbsd,
		// plan9, windows...
		fmt.Printf("%s.", os)
	}
}
```

We can still use `break` although it breaks at the end of every case.

> switch with no value is `switch true` and can be used to create long
> `if-then-else` chains.

``` go
package main

import (
	"fmt"
	"time"
)

func main() {
	t := time.Now()
	switch {
	case t.Hour() < 12:
		fmt.Println("Good morning!")
	case t.Hour() < 17:
		fmt.Println("Good afternoon.")
	default:
		fmt.Println("Good evening.")
	}
}
```

## defer

> A defer statement defers the execution of a function until the surrounding function returns.
>
> The deferred call's arguments are evaluated immediately, but the function call
> is not executed until the surrounding function returns.

In each block, every time we get to a defer, it is pushed into a stack. When the
function surrounding the block ends, then functions are popped from the stack
and executed.

``` go
package main

import "fmt"

func main() {
	defer fmt.Println("This runs after main")

	fmt.Println("Main ended")
}
```

-----------

# More types: structs, slices, and maps

## Pointers
I mean come on!!1! (John Oliver).

Similar to C:

* Point with `*`: `var p *int` == `int *p;`
* Generate pointer (get address of) with `&`: `i := 1` and `p = &i`

"Unlike C, Go has no pointer arithmetic." *Thanks*.

## Structs
Similar to C.

Do the field names need to be uppercase? It seems like. Because "lower case
fields (labels in general) are not visible outside the defining package, reflect
is outside."

``` go
package main

import "fmt"

type Student struct {
	FirstName string
	LastName string
}

func main() {
	fmt.Println(Student{"John", "Smith"})

	// But we usually want to make instances(?) of structs
	studentOne := Student{"Parsia", "H"}

	// Now we can access the fields using documents
	fmt.Println(studentOne.FirstName)

	// We can just assign fields using names, anything not assigned will be
	// initialized with zero as we have seen before
	studentTwo := Student{FirstName: "Ender"}

	// We will print "{Ender }" notice the space after Ender which is supposed
	// to be the delimiter between the fields, LastName is nil because it is not
	// given a value
	fmt.Println(studentTwo)	

	// Can make a pointer to a struct
	p := studentOne

	// Now instead of *p.LastName (doesn't work) we can just use p.LastName
	// fmt.Println((*p).LastName) will not work with error message: invalid indirect of p (type Student)
	fmt.Println(p.LastName)

	// Can just create a pointer out of the blue
	p2 := Student{"Hercule", "Poirot"}
	fmt.Println(p2)
}
```

## Arrays

`var a [10]int` == `int a[10];`.

Arrays cannot be resized.

``` go
package main

import "fmt"

func main() {
	var a [5]int
	a[0] = 10
	a[4] = 20
	fmt.Println(a)

	// We can initialize arrays during creation
	// str[3] is empty
	str := [3]string{"Ronny", "Johnson"}

	fmt.Println(str)
}
```

## Slices

> [Slice] is a dynamically-sized, flexible view into the elements of an array.
>
> The type `[]T` is a slice with elements of type `T`.

Seems like we can create a slice from members of an array.

Slices _don't store anything_, they reference the array. If we change something
via the slice, the array is modified.

``` go
package main

import "fmt"

func main() {
	// Our favorite characters from the ThatHappened subreddit
	// If we do not specify a length, it will create a slice literal and
	// an underlying array as we will see later
	thatHappened := [3]string{"RonnyJohnson", "AlbertEinstein", "MargaretHello"}

	// Last index is non-inclusive - should have guessed
	// allMembers []string := thatHappened[0:3]
	var allMembers []string = thatHappened[0:3]
	fmt.Println(allMembers)

	var lastTwoMembers []string = thatHappened[1:3]
	fmt.Println(lastTwoMembers)

	// Replace Ms.Hello with another popular character
	allMembers[2] = "JoeDisney"

	// Joe Disney added to the array
	fmt.Println(thatHappened)

	// The other slice changes
	fmt.Println(lastTwoMembers)

}
```

We can create array and slice literals. Meaning we can just initialize them by
their members instead of assigning a length and then adding members.

If a slice literal is created, the underlying array is also created. For now I
do not know how I can reference this underlying array (instead of using the
slice). I guess it's maybe impossible.

``` go
package main

import "fmt"

func main() {

	// Slice literal of type struct, the underlying array is created automatically
	sliceStruct := []struct {
		a,b int
	}{
		{1,2},
		{3,4},
		{5,6},	// need this comma in the end otherwise it will not work (why?)
	}

	fmt.Println(sliceStruct)

}
```

When creating an array, if we do not specify a length we will get a slice
literal as seen above.

If we do not want to specify a length we can use `[...]`.

``` go
package main

import "fmt"

func main() {

	thatHappened := [...]string{"RonnyJohnson", "AlbertEinstein", "MargaretHello"}

	// Joe Disney added to the array
	fmt.Println(thatHappened)

}
```

### Slice length and capacity
Slices have length and capacity.

* **Length** is the current number of items in the slice and can be returned via
  `len(slice)`.
* **Capacity** is the maximum number of items in the slice returned via
  `cap(slice)`. Capacity is the number of items in the original arrays from the
  start of the slice and *not the size of array*. For example if the slice
  starts from the second item of the array, its capacity is `len(array)-1`. This
  ensures that the slice cannot go past the array.

``` go
package main

import "fmt"

func main() {

	ints := [...]int{0, 1, 2, 3, 4, 5}
	fmt.Println(ints)

	slice1 := ints[2:6]

	// len=4 and cap=4 (from 3rd item of the array until the end)
	printSlice(slice1)

	slice1 = ints[2:4]

	// len=2 but cap will remain 4
	printSlice(slice1)
}

// Copied from the tour
func printSlice(s []int) {
	fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)
}

```

### make slices
To create dynamically-sized arrays use `make`. `make` creates a zero-ed array
and returns a slice to that array.

`slice1 := make([]int, 10)` creates an int array of length 10.

`slice2 := make([]int, 5, 10)` creates an int array of length 5 and capacity of 10.

We can **append** stuff to slices and it grows as needed.
`slice1 = append(slice1, 1)`. We can append multiple elements
`slice1 = append(slice1, 1, 2, 3)`.

In order to append one slice to the other (obviously they should be of the same
type), we have to use `...` like this: `slice1 = append(slice1, slice2...)`.

``` go
package main

import "fmt"

func main() {

	slice1 := make([]int, 10)
	printSlice(slice1)
	// len=10 cap=10 [0 0 0 0 0 0 0 0 0 0]

	slice2 := make([]int, 5, 10)
	printSlice(slice2)
	// len=5 cap=10 [0 0 0 0 0]

	slice3 := slice2[0:0]
	printSlice(slice3)
	// len=0 cap=10 []

	slice1 = append(slice1, 1, 2)
	printSlice(slice1)
	// len=12 cap=20 [0 0 0 0 0 0 0 0 0 0 1 2]

	slice1 = append(slice1, slice2...)
	printSlice(slice1)
	// len=17 cap=20 [0 0 0 0 0 0 0 0 0 0 1 2 0 0 0 0 0]
}

// Copied from the tour
func printSlice(x []int) {
	fmt.Printf("len=%d cap=%d %v\n", len(x), cap(x), x)
}
```

### Range
range iterates over slices. It returns an index and *a copy of the item* stored
at that index. `for index, value := range slice`.

`value` is optional but `index` is not. To not use `index` use `_`.

``` go
package main

import "fmt"

func main() {
	thatHappened := [3]string{"Ronny Johnson", "Albert Einstein", "Margaret Hello"}
	for index, value := range thatHappened {
		// No newline in the end of Printf but Println does not support formatting
		fmt.Printf("thatHappened[%d]: %s\n", index, value) 
	}

	fmt.Println("-----------")

	// Only using index
	for index := range thatHappened {
		fmt.Printf("thatHappened[%d]: %s\n", index, thatHappened[index])
	}

	fmt.Println("-----------")
	// Dropping index
	for _, value :=range thatHappened {
		fmt.Printf("%s\n", value)
	}
}
```

---------------

# Methods and interfaces

## Methods
Go doesn't have classes. Methods can be defined for types (e.g. structs). *what
is this? C?*

A method is a function with a special *receiver*, receiver is the type that this
method is defined for.

**How to do methods for slices:**
For example we can re-write the `printSlice` function and define it for slices
of type `int`.

Problem is `[]int` is an unnamed type and cannot be a receiver. We have to
create a type with that specific slice type (in this case `int`) like:
`type IntSlice []int`.

With a `value receiver` like what we have, operations are done on a *copy* of
the object.

``` go
package main

import "fmt"

type IntSlice []int

func (x IntSlice) PrintSlice() {
	fmt.Printf("len=%d cap=%d %v\n",
		len(x), cap(x), x)
}

func main() {

	var slice1 IntSlice = make([]int, 10)
	slice1.PrintSlice()	// len=10 cap=10 [0 0 0 0 0 0 0 0 0 0]

	var slice2 IntSlice = make([]int, 5, 10)
	slice2.PrintSlice()	// len=5 cap=10 [0 0 0 0 0]
}
```

### Pointer Receivers
Pointer receivers get a pointer instead of a value but can modify the object
that the pointer points to. Pointer receivers can be a pointer to a pointer
(e.g. `**int`).

By value receivers do not modify the object while by pointer receivers do.

In the following code, Tuple's fields will be modified by `ModifyTuplePointer()`
but not by `ModifyTupleValue()`.

However, **this is not the case for slices** (e.g. `IntSlice` in the code). Both
value and pointer receivers modify the slice. I do not know the reason but I
assume it's because the slice is already a reference to an array somewhere.

Pointer receivers are more efficient because they do not copy the original
object. Probably only matters when passing large structs.

**All methods for one type should either have value receivers or pointer receivers, do not mix and match like the code below :).**

``` go
package main

import "fmt"

type Tuple struct {
	A, B int
}

// Should not change the value of the object as it works on a copy of it
func (x Tuple) ModifyTupleValue() {
	x.A = 2
	x.B = 2
}

// Should change the value of the object
func (x *Tuple) ModifyTuplePointer() {
	x.A = 3
	x.B = 3
}

type IntSlice []int

func (x IntSlice) PrintSlice() {
	fmt.Printf("len=%d cap=%d %v\n",
		len(x), cap(x), x)
}

// Modifies the IntSlice although it's by value
func (x IntSlice) ModifySliceValue()  {
	x[0] = 1
}

// Modifies the IntSlice
func (x *IntSlice) ModifySlicePointer()  {
	(*x)[0] = 2
}

func main() {

	nem := Tuple{1, 1}

	nem.ModifyTupleValue()
	fmt.Println(nem)	// {1 1}


	nem.ModifyTuplePointer()
	fmt.Println(nem)	// {3 3}

	var slice1 IntSlice = make([]int, 5)
	slice1.PrintSlice()	// len=5 cap=5 [0 0 0 0 0]


	slice1.ModifySliceValue()
	slice1.PrintSlice()	// len=5 cap=5 [1 0 0 0 0]

	slice1.ModifySlicePointer()
	slice1.PrintSlice()	// len=5 cap=5 [2 0 0 0 0]
}
```

## Interfaces

> An _interface type_ is defined as a set of method signatures.
>
> A value of interface type can hold any value that implements those methods.

For example we will define an interface which has the method `MyPrint()`, now
each type that has that method can be assigned to an interface of that type

``` go
package main

import "fmt"

type MyPrinter interface {
	MyPrint()
}

type MyInt int

func (i MyInt) MyPrint() {
	fmt.Println(i)
}

type MyFloat float64

func (f MyFloat) MyPrint() {
	fmt.Println(f)
}

func main() {

	var thePrinter MyPrinter

	float1 := MyFloat(1.2345)
	int1 := MyInt(10)

	thePrinter = float1
	thePrinter.MyPrint()
	// 1.2345

	thePrinter = int1
	thePrinter.MyPrint()
	// 10

}
```

**Empty Interface** is `interface {}` and can hold any type. Usually used to
handle unknown types.

``` go
package main

import "fmt"

var emptyInterface interface{}

type Tuple struct {
	A, B int
}

func main() {

	// Use int
	int1 := 10
	emptyInterface = int1
	fmt.Println(emptyInterface)
	// 10

	// Use float
	float1 := 1.2345
	emptyInterface = float1
	fmt.Println(emptyInterface)
	// 1.2345

	// Use custom struct
	tuple1 := Tuple{5, 5}
	emptyInterface = tuple1
	fmt.Println(emptyInterface)
	// {5 5}

}
```

We can access the value inside the interface like this
`myFloat := myInterface(float64)`. If the interface does not contain a float,
this will trigger a panic.

In order to handle it properly we use it like this
`myFloat, ok := myInterface(float64)`. This will prevent the panic. If the
interface has a float, `ok` will be `true` and otherwise `false`.

``` go
package main

import "fmt"

func main() {
	var myInterface interface{} = 1234.5

	myFloat, ok := myInterface.(float64)
	fmt.Println(myFloat, ok)
	// 1234.5 true

	myInt, ok := myInterface.(int)
	fmt.Println(myInt, ok)
	// 0 false -- which means it does not contain an int

	// This will trigger a panic
	// myInt = myInterface.(int)
}
```

### Type switch
Do a switch on `interface.(type)`. Similar to what we did above.

``` go
// Code copied from the tutorial
package main

import "fmt"

func do(i interface{}) {
	switch v := i.(type) {
	case int:
		fmt.Printf("Twice %v is %v\n", v, v*2)
	case string:
		fmt.Printf("%q is %v bytes long\n", v, len(v))
	default:
		fmt.Printf("I don't know about type %T!\n", v)
	}
}

func main() {
	do(21)		// Twice 21 is 42
	do("hello")	// "hello" is 5 bytes long
	do(true)	// I don't know about type bool!
}
```

### Stringers
Defined by the `fmt` package. Can describe itself as string.

``` go
type Stringer interface {
    String() string
}
```

If we implement it for any struct, it will be called when calling `Println` (and
others) on it. Essentially create a method for that struct named `String()`
which returns a `string`.

This is also what gets printed when we want to print an instance of that type
with the `%v` format string ~~switch~~ verb.

``` go
package main

import "fmt"

type Tuple struct {
	A, B int
}

func (t Tuple) String() string {
	return fmt.Sprintf("A: %d, B: %d", t.A, t.B)
}

func main() {

	tuple1 := Tuple{10, 10}
	tuple2 := Tuple{20, 20}
	fmt.Println(tuple1)	// A: 10, B: 10
	fmt.Println(tuple2)	// A: 20, B: 20
}
```

## Solution to the Stringers exercise

``` go
package main

import "fmt"

type IPAddr [4]byte

// TODO: Add a "String() string" method to IPAddr.
func (ip IPAddr) String() string {
	return fmt.Sprintf("%v.%v.%v.%v", ip[0], ip[1], ip[2], ip[3])
}

func main() {
	hosts := map[string]IPAddr{
		"loopback":  {127, 0, 0, 1},
		"googleDNS": {8, 8, 8, 8},
	}
	for name, ip := range hosts {
		fmt.Printf("%v: %v\n", name, ip)
	}
}
```

## Errors
`error` type is similar to `Stringer()`.

``` go
type error interface {
    Error() string
}
```

Create a method for the struct type named `Error()` to return error codes/messages.

``` go
func (e MyType) Error() string {
	return fmt.Sprintf("Error message")
}
```

Most built-in and package methods return an error value if an error occurs,
otherwise they will return `nil` for error which means no error.

## Solution to the Errors exercise

``` go
package main

import "fmt"

type ErrNegativeSqrt float64

func (e ErrNegativeSqrt) Error() string {
	return fmt.Sprintf("cannot Sqrt negative number: %v", float64(e))
}

func Sqrt(x float64) (float64, error) {

	if (x < 0) {
		return 0, ErrNegativeSqrt(x)
	}

	// Don't need else here
	return 0, nil
}

func main() {
	fmt.Println(Sqrt(2))
	fmt.Println(Sqrt(-2))
}
```

_Skipped the rest of the module._

----------------------

# Concurrency

`go function(a, b)` runs the function in parallel and continues with the rest of
the program.

## Channels
Typed conduit. Support sending and receiving values using `<-`.

Channels must be created before use.

> By default, sends and receives block until the other side is ready.

``` go
// Make a channel of type int in honor of the famous hacker
// Note that we can only send/receive int via this channel
fourChan := make(chan int)

// Send to channel
fourChan <- someInt

// Receive data from channel
newInt := <- fourChan
```

### Buffered channels
If channels are `buffered` then they will only block when the buffer is full.
`fiveChan := make (chan int, 100)` will create a channel with a buffer size of
`100`.

### Closing channels
To test if a channel is closed do `someInt, ok := <- fourChan`. If channel is
not closed, ok with be `true`, otherwise `false` means channel is closed.
Sending items to a closed channel will cause a panic.

To close a channel do `close(fourChan)`.

### Reading information from channels
Use a `range` in a `for` to receive values from the channel in a loop until it
closes like `for i:=range fourChan`. If you want to read something from an open
channel and there's nothing there, the program will block(?) and wait until it
gets something.

### select
`select` has some `case`s. It will block until one of the cases is ready and
runs it. If multiple are ready, it will choose one at random.

``` go
select{
case fourChan <- x:
	// Whatever
case c <- fiveChan:
	// Whatever
default:
	// This is run if no other case is ready
}
```

## sync.Mutex
`sync.Mutex` has two methods, `lock` and `unlock`. We can also `defer` the
`unlock` if we want to return something and then unlock it like the `Value`
method from the example.

``` go
// Value returns the current value of the counter for the given key.
func (c *SafeCounter) Value(key string) int {
	c.mux.Lock()
	// Lock so only one goroutine at a time can access the map c.v.
	defer c.mux.Unlock()
	return c.v[key]
}
```

----------

# Printf from Go by example
Taken from `Go by Example` and `Effective Go`.

These three need a format string:

* `fmt.Sprintf` returns a string.
* `fmt.Fprintf` takes any objects that implements `io.Writer` for example
  `os.Stdout` and `os.Stderr`.
* `fmt.Printf` prints to stdout(?).

The following are similar to the above but do not need a format string:

* `fmt.Print` and `fmt.Println`.
* `fmt.Fprint` - `fmt.Fprint(os.Stdout, "Ronny", "Johnson", "$100%")`.
* `fmt.Sprint`.

## ~~Switches~~ Verbs
Better info here: https://golang.org/pkg/fmt/#hdr-Printing

### Decimals
`%d`: digits = numbers.

`%nd`: n = width of number. Right justified and padded with spaces. To left
justify use `-` like `%-nd`. If n is less than the number of digits nothing
happens.

`%b`: number in binary.

`%c`: `chr(int)`, prints the character corresponding to the number.

`%x`: hex.

### Floats
`%f`: float.

`%n.mf`: n = decimal width, m = float width. Right justified. To left justify
use `-` like `%-n.mf`. If n is less than the number of digits nothing happens.

`%e` and `%E`: scientific notation (output is a bit different from each other).

### Value
`%v` or value: catch all format. Will print based on value.

`%+v`: will print struct's field names if we are printing a struct. Has no
effect on anything else.

`%#v`: prints a "Go syntax representation of the value, i.e. the source code
snippet that would produce that value." For example for a struct instance it
will give code that creates such a struct instance and initializes it with the
current values of the struct instance.

### Strings
`%q`: "To double-quote strings as in Go source, use `%q`."

`%s`: string.

`%ns`: control width of string. Right justified, padded with spaces. To left
justify use `-` like `%-ns`. If n is less than the length of the string, nothing
happens.

### Others

`%t`: boolean.

`%T`: prints the type of a value. For example `int` or `main.myType`.

``` go
package main

import "fmt"

type myType struct {
	field1 int
	field2 string
	field3 float64
}

func main() {

	// struct type
	struct1 := myType{10, "Ronny", -10.2}
	fmt.Printf("%v\n", struct1)		// {10 Ronny -10.2}
	fmt.Printf("%+v\n", struct1)	// {field1:10 field2:Ronny field3:-10.2}
	fmt.Printf("%#v\n", struct1)	// main.myType{field1:10, field2:"Ronny", field3:-10.2}
	fmt.Printf("%T\n", struct1)		// main.myType

	// int
	int1 := 123
	fmt.Printf("%v\n", int1)		// 123
	fmt.Printf("%d\n", int1)		// 123
	fmt.Printf("|%6d|\n", int1)		// |   123|
	fmt.Printf("|%-6d|\n", int1)	// |123   |
	fmt.Printf("%T\n", int1)		// int
	fmt.Printf("%x\n", int1)		// 7b
	fmt.Printf("%b\n", int1)		// 1111011
	fmt.Printf("%e\n", int1)		// %!e(int=123)
	fmt.Printf("%c\n", int1)		// {

	// float
	float1 := 1234.56
	fmt.Printf("%f\n", float1)			// 1234.560000
	fmt.Printf("|%3.2f|\n", float1)		// |1234.56|
	fmt.Printf("|%-3.2f|\n", float1)	// |1234.56|
	fmt.Printf("%e\n", float1)			// 1.234560e+03
	fmt.Printf("%E\n", float1)			// 1.234560E+03

	// string
	string1 := "Ronny"
	fmt.Printf("%s\n", string1)			// Ronny
	fmt.Printf("|%10s|\n", string1)		// |     Ronny|
	fmt.Printf("|%-10s|\n", string1)	// |Ronny     |
	fmt.Printf("%T\n", string1)			// string

	// boolean
	boolean1 := true
	fmt.Printf("%t\n", boolean1)	// true
	fmt.Printf("%T\n", boolean1)	// bool

}
```


# Maps
Go map == hash table. Fast lookup/add/delete. Each key is associated with a
value (Python dict?).

Declare an initialized map: `mapName := make(map[KeyType]ValueType)`. `KeyType`
needs to be a `comparable` type. `ValueType` can be anything.

If a key does not exist, the result is a zero value. For example `0` for `int`.

To check if a key exists or not (0 might be a valid value in the map)
`value, ok := mapName[key]`. If `ok` is true then the key exists (and false if
the key is not there).

To test for a key without getting the value drop the value like this
`_, ok := mapName[key]` and then just check `ok`.

`range` iterates over the contents of a map as we have seen before for
arrays/slices. In this case we get keys instead of indexes. Use it with a `for`.

`for key, value := range mapName`.

We can initialize a map using data.

We can also initialize an empty map instead of the `make` (`mapName = map[KeyType]ValueType{}`).

-----

<!-- Other tips and tricks -->

# Other tips and tricks

## Errors
To do a custom error, import the `errors` package and use it like this.

``` go
package main

import "errors"

func randomFunction() (return1 interface{}, err error) {
	// Whatever
	var result interface{}
	return result, errors.New("Custom error string")
}
```

## Hexdump
`encoding/hex` package is your friend: https://golang.org/pkg/encoding/hex/.

`encoding/hex.Dump` - `func Dump(data []byte) string`: Returns a string
containing a normal hex dump (e.g. offset - hex - printable characters).
Internally it calls the `Dumper` function -
[source](https://golang.org/src/encoding/hex/hex.go?s=2676:2705#L93).

`encoding/hex.Dumper` - `func Dumper(w io.Writer) io.WriteCloser`: Returns an
`io.WriteCloser` (I don't know exactly what it is, but it seems like we can call
`Write`)

Seems like there is no way to remove the offset. Either I can modify the
[source](https://golang.org/src/encoding/hex/hex.go?s=3321:3375#L133) or write
my own. There's also this [MIT licensed package](https://github.com/glycerine/golang-hex-dumper)
that looks easier to modify. In both cases, the modification looks pretty straightforward.

## Named imports
We can do named imports like Python.

``` go
package main

import (
	thisIsFMT "fmt"
)

func main() {
	thisIsFMT.Println("whatever")
}
```

## Importing a package into the current namespace
Using `import . "packagename"` means we can omit the package name. In the
example below we can omit `fmt`.

No clue how name collisions are handled (e.g. two packages imported into the
namespace having the same function name).

``` go
package main

import (
	. "fmt"
)

func main() {
	Println("whatever")
}
```

## Avoiding the damn unused warnings
Yeah it's nice to get "better" code (although that is debatable but I am not a
dev so I am biased), but it's a pain when debugging/testing. Send them to `_`.

``` go
package main

import (
    _ "package name" // gone to the dogs
)

func main() {
    unUsedVar := "whatever"
    _ = unUsedVar	// gone to the dogs
}
```

## Unix Timestamp to String

``` go
import "strconv"

strconv.FormatInt(time.Now().Unix(), 10)
```

## Spawn a new thread (goroutine) on the spot

``` go
func main() {

	// Whatever

	go func() {
		// Whatever happens in this goroutine
	}()

}
```

## Write to a file or io.buffer from goroutines - DON'T
Instead use a buffered channel (will make it async). Make a channel before
goroutines, send stuff to the channel from goroutines. Make another goroutine
that creates a file, does `defer fileHandle.Close()` (which makes closes the
file after this goroutine ends) and then has an infinite loop where it reads
from the channel and writes to a file.

``` go
// ...
// Logging channel- buffered so it's async
fourChan := make(chan string, 100)

go func() {
	for {
			// Do something and get a string
			fourChan <- string1
		}
	}
}()

go func() {
	for {

		// Do something else
		fourChan <- string2
		}
	}
}()

go func() {
	// Get a unique filename
	dumpFile, _ := os.Create("whatever.txt")
	defer dumpFile.Close()  // finally a good use for defer
	for {
		dumpFile.WriteString(<- fourChan)
	}
}()
// ...
```

## Generate godoc HTML for a Single Package
If godoc doesn't run locally because not all of your packages can be built
(which is normal), create the HTML output for one single package to inspect:

```
godoc -html cmd/github.com/user/package > package-godoc.html
```

-----

# Stuff learned from Cryptopals
I learned a bunch after I returned to go after a while and tried to do the
Cryptopals challenge.

## Long string on multiple lines

``` go
const Input = "49276d206b696c6c696e6720796f7572" +
              "20627261696e206c696b65206120706f" +
              "69736f6e6f7573206d757368726f6f6d"
```

## Compare two []bytes with bytes.equal
Works with slices too.

Use `bytes.equal`:

``` go
package main

import (
	"bytes"
	"fmt"
)

func main() {

	bytes1 := []byte("Hello")
	bytes2 := []byte("Hello")
	bytes3 := []byte("Bye")

	if eval := bytes.Equal(bytes1, bytes2); eval {
		fmt.Println("1 and 2 are equal")
	} else {
		fmt.Println("1 and 2 are different")
	}

	if eval := bytes.Equal(bytes2, bytes3); eval {
		fmt.Println("2 and 3 are equal")
	} else {
		fmt.Println("2 and 3 are different")
	}
}
```

## Sorting a array/slice of struct by field
Code from [https://stackoverflow.com/a/28999886](https://stackoverflow.com/a/28999886).

Arrays need to be passed through a slice but the underlying array will also be sorted.

``` go
type MyObj struct {
    Name string
    Score int
    Code []byte
}

myObjects := make([]MyObj, 10)

// ...

// Sort by Score
// We are passing a slice before sorting but underlying array will be sorted
sort.Slice(myObjects[:], func(i, j int) bool {
    return myObjects[i].Score < myObjects[j].Score
})
```

## Append two slices
With [append](https://golang.org/pkg/builtin/#append) you can append a slice and
a primitive of that slice. For example to append a []byte with a byte you can
do:

``` go
package main

import "fmt"

func main() {
	bytes := []byte("Some string")
	byte1 := byte(0x31)

	bytes = append(bytes, byte1)
	
	fmt.Println(string(bytes))
}

// Some string1
```

Now if we want to append two slices (e.g. two `[]byte`s) we need to do a bit of
magic because the second argument to append needs to be a `byte`:

``` go
package main

import "fmt"

func main() {
	bytes1 := []byte("Some string")
	bytes2 := []byte(" Another string")

	bytes1 = append(bytes1, bytes2)
	
	fmt.Println(string(bytes1))
}
```

We will get this error:

- cannot use bytes2 (type []byte) as type byte in append

What we can do is pass the second slice with `...`. I am not quite sure how this
works but it seems like we are passing the slice as a collection of all of its
members


``` go
package main

import "fmt"

func main() {
	bytes1 := []byte("Some string")
	bytes2 := []byte(" Another string")

	bytes1 = append(bytes1, bytes2...)
	
	fmt.Println(string(bytes1))
}

// Some string Another string
```

According to the documentation "As a special case, it is legal to append a
string to a byte slice, like this:""

- `slice = append([]byte("hello "), "world"...)"`

# Generics
~~lol no generics~~!

## Diff Two Generic Slices

```go
func diffSlice[E comparable](first, second []E) (missing []E) {
	for _, item := range first {
		if !slices.Contains(second, item) {
			missing = append(missing, item)
		}
	}
	return
}
```

## Nil Generic Slice and Map

```go
// nilSlice creates a nil slice of type t.
func nilSlice[T any]() []T {
	var t []T
	return t
}
```

Unfortunately, the `map` is not as simple. This function technically creates a
`nil` map but it's useless.

```go
// nilMap creates a nil map[T1]T2.
func nilMap[T1 comparable, T2 any]() map[T1]T2 {
	var m map[T1]T2
	return m
}
```

We cannot do `make(m, 0)` because it's not a type. We cannot assign items to it
because it's not initialized.

```go
myMap := nilMap[string, string]()

// error here - assignment to entry in nil map
myMap["1"] = "val"
```

We have to assign an empty map to it:

```go
myMap := nilMap[string, string]()
myMap = map[T1]T2{}
myMap["1"] = "val"
```

So instead we return an empty map.

```go
// emptyMap creates an initialized empty map[T1]T2.
func emptyMap[T1 comparable, T2 any]() map[T1]T2 {
	return map[T1]T2{}
}
```