---
draft: false
toc: true
comments: false
categories:
- Development
title: "Rust"
wip: false
snippet: "Rust notes - Code is at [https://github.com/parsiya/fearless-concurrency](https://github.com/parsiya/fearless-concurrency)"
---

# Learning Rust

* "The book": https://doc.rust-lang.org/stable/book/
* Playground: https://play.rust-lang.org/

Install Rust in WSL (from https://www.rust-lang.org/tools/install):

* `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

# Chapter 1

```
cargo whatever
# create a package in `whatever` directory under the current path.
`whatever/src/main.rs` will have `hello world`.

cd whatever

cargo check     # check if it compiles without building

cargo building  # build the package

cargo run       # run
```

# Chapter 2
Every variable is immutable, have to make it mutable with `mut`:
`let mut something = 1;`

References passed to functions can also be mutable or not regardless of the
underlying variable. E.g., we can create an immutable reference to a mutable
variable. In the code below `read_line` needs a `mut string`, so we pass
`&mut guess` instead of just `&guess`.

`read_line` appends whatever is read from the command line to the argument. It
does not overwrite anything. Here, it doesn't matter because `guess` is empty.

```rs
use std::io;

fn main() {
    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    println!("You guessed: {}", guess);
}
```

`expect`: The result of `read_line` is an enum of type `io::Result`. It can be
`Ok` or `Err`. If the value is `Err` then `expect` is called that crashes the
program and displays the message passed to it (`Failed to`). If the value is
`Ok` then `expect` will return the number of bytes read which we are not using
here. We can use it like this:

```rs
let bytes = io::stdin()
    // Read from input and append to guess.
    .read_line(&mut guess)
    .expect("Failed to read line");

println!("Read {} bytes", bytes);
```

Finally, we have the placeholder similar to `printf(%v)` in Go.

## Dependencies
Edit `Cargo.toml` and add dependencies like `rand = "0.8.3"`. Then `cargo build`.

`cargo update` ignores `Cargo.lock` and grabs the latest versions of libraries
(that fit the versions specified in `Cargo.toml`).

Now, we can use `rand` here like this:

```rs
use rand::Rng;

fn main() {
    println!("Guess the number!");

    // Generate a "random" number between 1 and 100.
    // Alternative param to "1..101" is "1..=100".
    let secret_number = rand::thread_rng().gen_range(1..101);
    // removed
}
```

`1..101` range == `[1, 101)` == number between 1 and 100 == `1..=100`.

The VS Code Rust language server shows us the docs for methods (and does other
things like autocomplete), but it's also possible to see the crate docs with
`crate doc --open`. This will build the docs for each of the dependencies and
open them in the browser.

To do a comparison, we add `std::cmp::Ordering` which is another enum with three
values: `Less/Greater/Equal`.

```rs
// ch02/guessing_game/src/main.rs
use std::cmp::Ordering;

fn main() {
    // removed

    // Create a mutable string.
    let mut guess = String::new();

    let bytes = io::stdin()
        // Read from input and append to guess.
        .read_line(&mut guess)
        .expect("Failed to read line");
    
    // cmp compares two values
    match guess.cmp(&secret_number) {
        Ordering::Less => println!("Too small!"),
        Ordering::Greater => println!("Too big!"),
        Ordering::Equal => println!("You win!"),
    }
    // removed
}
```

`cmp` compares two values. Usable on anything that can be compared. The result
is an enum of `Ordering`. We can use the `match` to do something based on what
was returned. In this case we have three `arms` (choices). Each arm has a
`pattern` (e.g., `Ordering::Less`) and an action `println!`.

This won't compile because `secret_number` is of type `integer` and `guess` is a
`string` so we cannot compare them.

```rs
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

Instead of creating a new variable to store `guess` converted to an integer, we
can `shadow` the previous value. This allows us to reuse the variable name and
usually used in situations like this.

`guess.trim()` removes whitespace before/after the string. The string has the
new line character(s) because we pressed enter to finish it so it must be
trimmed.

`.parse()` converts a string into a number. To tell Rust which kind of number,
we annotate the variable with `let guess: u32`.

`.expect` returns the error if `parse` returns an error and the converted number
if the return value is `Ok`.

## Adding a Loop
We can do an infinite loop with

```rs
loop {
    println!("Please input your guess.");

    // removed

    println!("You guessed: {}", guess);
}
```

We can break out of it with `break`. We want to leave the loop when we guess the
number correctly so we add to the actions for the `Ordering::Equal` arm.

```rs
match guess.cmp(&secret_number) {
    Ordering::Less => println!("Too small!"),
    Ordering::Greater => println!("Too big!"),
    Ordering::Equal => {
        println!("You win!");
        break;
    }
}
```

## Handling Invalid Input
Entering a non-number will crash the program. Let's handle it. Instead of
calling `expect` we `match` on the return value of `parse`.

```rs
let guess: u32 = match guess.trim().parse() {
    Ok(num) => num,     // If parse worked correctly, store the number in guess.
    Err(_) => continue, // If parse returned an error, go back to the beginning of the loop.
};
```

If `parse` worked correctly it returns an `Ok` value that contains the number.
Otherwise, it returns an `Err` with the error message. In `Err(_)` we are
catching every message (with `_`).

# Chapter 3
Some programming concepts in Rust.

## Mutability
We already know this. Every variable is immutable unless we use `mut`. If we
want to modify an immutable variable, the compiler warns us and does not compile
the program. See [ch03/variables/src/main.rs](ch03/variables/src/main.rs).

## Constants
Created with `const` keyword. We cannot use `mut` with them because they are
always immutable. Can only be set to a constant expression not something that is
calculated at runtime.

```rs
const FIRST_NAME = "Parsia";
const TIME: u32 = 10 * 20 * 30;
```

Naming convention: All uppercase with underscore between words.

## Shadowing
Declare a variable with the same name. Interestingly, this can be done in
specific scopes. E.g., we can shadow a variable inside a block but it will not
be modified outside.

```rs
// ch03/shadowing/src/main.rs
fn main() {
    let x = 5;
    
    let x = x + 1; // x = 6
    // Seems like we can just create random blocks here.
    {
        let x = x * 2;  // x = 12
        // x is only shadowed in this scope.
        println!("The value of x in the inner scope is: {}", x);
    }
    // x = 6 because this one is not touched.
    println!("The value of x is: {}", x);
}
```

Seems like we can just make blocks with `{ }`.

Differences with `mut`:

1. We can shadow an immutable variable and create an immutable variable with the
   same name.
2. We can change the type and reuse the name. We cannot change the type of a
   mutable variable.

This works because we are shadowing `spaces` and creating a new variable of type
int.

```rs
fn main() {
    let spaces = "   ";
    let spaces = spaces.len();
}
```

We can also make the new `spaces` mutable:

```rs
// ch03/shadowing2/src/main.rs
fn main() {
    let spaces = "   ";
    println!("spaces: {}", spaces);
    let mut spaces = spaces.len();
    println!("spaces: {}", spaces);
    spaces = 1234;
    println!("spaces: {}", spaces);
}
```

returns:

```
spaces: [prints three spaces]
spaces: 3
spaces: 1234
```

If we make a variable mutable but do not modify it, the compiler will give us a
warning saying it should not be mutable.

```rs
fn main() {
    let spaces = "   ";
    println!("spaces: {}", spaces);
    let mut spaces = spaces.len();
    println!("spaces: {}", spaces);
}
```

The shadowing `spaces` (2nd one) is mutable but not modified so we get:

```
Compiling playground v0.0.1 (/playground)
warning: variable does not need to be mutable
 --> src/main.rs:4:9
  |
4 |     let mut spaces = spaces.len();
  |         ----^^^^^^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default

warning: `playground` (bin "playground") generated 1 warning
    Finished dev [unoptimized + debuginfo] target(s) in 1.79s
     Running `target/debug/playground`
Standard Output
spaces:    
spaces: 3
```

## Integers
Like we have seen before. We can have 8, 16, 32, 64, and 128-bit integers.
Default is `i32`.

* Signed: `i8 i16 i32 i64 i128`
* Unsigned: `u8 u16 u32 u64 u128`

There's also `isize` (signed) and `usize` (unsigned) which are based on the
machine. E.g., i64 for 64-bit machines.

When writing integer literals we can use some help:

* `_` is ignored so `1_200` and `1200` are equal.
* Start
    * Hex number with `0x`: `0xAB`.
    * Octal number with `0o` (zero and the letter `o`): `0o77`.
    * Binary number with `0b`: `0b0011_1111`. See the `_` for better readability.
    * Byte with `b` (only `u8`): `b'A'`.

## Floating Point
`f32` and `f64` (default). To specify `f32` we need to annotate it:

```rs
fn main() {
    let x = 2.0; // f64

    let y: f32 = 3.0; // f32
}
```

## Numeric Operations
As you can imagine.

```rs
// ch03/numeric_operations.rs
fn main() {
    // addition
    let sum = 5 + 10;
    println!("5 + 10 = {}", sum); // 5 + 10 = 15

    // subtraction
    let difference = 95.5 - 4.3;
    println!("95.5 - 4.3 = {}", difference); // 95.5 - 4.3 = 91.2

    // multiplication
    let product = 4 * 30;
    println!("4 * 30 = {}", product); // 4 * 30 = 120

    // division
    let quotient = 56.7 / 32.2;
    let floored = 2 / 3; // Results in 0
    println!("56.7 / 32.2 = {}", quotient); // 56.7 / 32.2 = 1.7608695652173911
    println!("2 / 3 = {}", floored); // 2 / 3 = 0

    // remainder
    let remainder = 43 % 5;
    println!("43 % 5 = {}", remainder); // 43 % 5 = 3
}
```

## Boolean
`true` and `false`.

## Character Type
`char`: 4-bytes Unicode Scalar values. E.g., `U+0031` or emojis.

Used with `'` (strings use `"`).

## Tuple
Fixed-size array/slice of values with different types.

```rs
// ch03/tuple.rs
fn main() {
    // create a tuple like this, note the type annotation.
    let tup: (i32, f64, u8) = (500, 6.4, 1);

    // destructure it to get the values.
    let (x, y, z) = tup;
    println!("x = {}, y = {}, z = {}", x, y, z);
    // x = 500, y = 6.4, z = 1

    // can also get the value by `var.index`.
    println!("tup.0 = {}, tup.1 = {}, tup.2 = {}", tup.0, tup.1, tup.2); 
    // tup.0 = 500, tup.1 = 6.4, tup.2 = 1
}
```

## Array
Fixed-size array of values with the same type. Goes on stack instead of heap.

```rs
// ch03/arrays.rs
fn main() {
    let arr = [1, 2, 3];
    println!("arr = {:?}", arr);
    let strings = ["one", "two", "three"];
    println!("strings = {:?}", strings);

    // we can also specify the type and size. See below why we are using &str here.
    let arr2: [&str; 3] = ["one", "two", "three"];
    println!("arr2 = {:?}", arr2);
}
```

Specify one initial value for all elements:

```rs
// these are the same
let a = [3; 5];
let b = [3, 3, 3, 3, 3];
```

Access array elements like most other languages:

```rs
let arr = [1, 2, 3];
let b = arr[0]; // b = 1;
```

It's possible to access elements beyond the capacity. If the value is known when
compiling, the Rust compiler will give us an error:

```rs
fn main() {
    
    let arr2: [&str; 3] = ["one", "two", "three"];
    println!("arr2 = {:?}", arr2);
    
    println!("arr2[3] = {}", arr2[3]);
                         //  ^^^^^^^ index out of bounds: the length is 3 but the index is 3
    
    let c = 1 + 2;
    println!("arr2[c] = {}", arr2[c]);
                         //  ^^^^^^^ index out of bounds: the length is 3 but the index is 3
}
```

However, we can provide a dynamic variable (e.g., get it from the user) and the
program will panic with an out of bounds access.

## String Literals
So I had this problem above, when you create something like this
`let a = "whatever";` you are creating a `string literal` or `&str` which is a
read-only string and not the same as the type `String`.

So when I wanted to annotate the type for the same array like this, I got an
error:

```rs
let arr2: [str, 3] = ["one", "two", "three"];
                      ^^^^^ expected `str`, found `&str`
```

So we have to annotate it like this with `&str` but I had another problem
printing it:

```rs
let arr2: [&str, 3] = ["one", "two", "three"];
println!("arr2 = {}", arr2);
                      ^^^^ `[&str; 3]` cannot be formatted with the default formatter
  = help: the trait `std::fmt::Display` is not implemented for `[&str; 3]`
  = note: in format strings you may be able to use `{:?}` (or {:#?} for pretty-print) instead
```

We can use the note to pretty print:

```rs
println!("arr2 = {:?}", arr2);
// arr2 = ["one", "two", "three"]

println!("arr2 = {:#?}", arr2);
// arr2 = [
//     "one",
//     "two",
//     "three",
// ]
```

## Functions
Similar to other languages.

```rs
fn main() {
    my_func(10, 'a');
}

// we can define parameters.
fn my_func(param1: i32, param2: char) {
    println!("param1 = {}, param2 = {}", param1, param2);
    // param1 = 10, param2 = a
}
```

The last expression in the function can act as the return value.

> blocks of code evaluate to the last expression in them, and numbers by
> themselves are also expressions

```rs
fn main() {
    println!("double_me(1) = {}", double_me(1)); // double_me(1) = 2
}

// return values
fn double_me(x: i32) -> i32 {
    x + 1
}
```

However, if we change it to `x + 1;` it becomes an statement and we get an
error.

```
  |
6 | fn double_me(x: i32) -> i32 {
  |    ---------            ^^^ expected `i32`, found `()`
  |    |
  |    implicitly returns `()` as its body has no tail or `return` expression
7 |     x + 1;
  |          - help: consider removing this semicolon
```

Instead, we can use the `return` keyword.

```rs
fn main() {
    println!("double_me(1) = {}", double_me(1));
}

// return values
fn double_me(x: i32) -> i32 {
    return x + 1;
}
```

## if-else
Similar to other languages.

```rs
fn main() {
    let number = 3;

    if number < 5 {
        println!("less than five");
    } else if number == 5 {
        println!("equals five");
    } else if number > 5 {
        println!("more than five");
    }
}
```

Doing unneeded parentheses around the condition returns a warning
(e.g., `if (number < 5)`):

```rs
  |
4 |     if (number < 5) {
  |        ^          ^
  |
  = note: `#[warn(unused_parens)]` on by default
help: remove these parentheses
  |
4 -     if (number < 5) {
4 +     if number < 5 {
  | 
```

We can use `if` in a `let` statement:

```rs
fn main() {
    let condition = true;
    let number = if condition { 5 } else { 6 };

    println!("The value of number is: {}", number);
}
```

## loop
We've already seen it. `loop` can use `break` and `continue` to leave to go back
to the start. When loops are nested, these only apply only to their parent loop.

We can also have `labeled loops` so we can interact with outer loops

```rs
// ch03/labeled_loop.rs
fn main() {
    let mut count = 0;
    'parent_loop: loop {
        println!("count = {} in 'parent_loop", count);

        loop {
            println!("count = {} in inside loop", count);
            if count == 2 {
                // break out of the 'parent_loop
                break 'parent_loop;
            }
            count += 1;
        }
    }
    println!("End count = {}", count);
}

// count = 0 in 'parent_loop
// count = 0 in inside loop
// count = 1 in inside loop
// count = 2 in inside loop
// End count = 2
```

We can also return values from loop (lol wut?). We can assign the loop to a
variable and then return `break value;`.

```rs
// ch03/return_value_loop.rs
fn main() {
    let mut count = 0;

    let counted = loop {
        count += 1;
        if count == 5 {
            break count;
        }
    };

    println!("counted = {}", counted); // counted = 5
}
```

## while
`loop`s don't have conditions. We can use `while` instead.

```rs
// ch03/while.rs
fn main() {
    let mut count = 0;

    while count != 5 {
        count += 1;
    }

    println!("count = {}", count); // count = 5
}
```

## Loop Through Collections with for
We can iterate through a collection (e.g., array but not tuple) with `for`.

```rs
// ch03/while.rs
fn main() {
    let strings = ["one", "two", "three"];

    for s in strings {
        println!("{}", s);
    }
}
```

Trying to use `for` with a tuple returns this error.

```rs
let tup: (i32, f64, u8) = (500, 6.4, 1);

for t in tup {
    println!("{}", t);
}

    |
10  |     for t in tup {
    |              ^^^ `(i32, f64, u8)` is not an iterator
    |
    = help: the trait `Iterator` is not implemented for `(i32, f64, u8)`
    = note: required because of the requirements on the impl of `IntoIterator` for `(i32, f64, u8)`
note: required by `into_iter`
```

The book says `for` is the most common way to use loops. We can use it to repeat
things a certain number of times by using it over a range.

```rs
// rev is reversing the range.
fn main() {
    for number in (1..4).rev() {
        println!("{}!", number);
    }
    println!("LIFTOFF!!!");
}

// 3!
// 2!
// 1!
// LIFTOFF!!!
```

# Chapter 4
Stack: LIFO. Data on stack must have a known and fixed size. Faster.

Heap: Data with unknown size at compile time or a size that might change. You
ask for a certain amount of space on heap, the memory allocator locates some
free space and returns a pointer to it (and sets it in-use). Slower.

## Ownership Rules

* Each value in Rust has a variable that’s called its *owner*.
* There can only be one owner at a time.
* When the owner goes out of scope, the value will be dropped.

## The String Type
String literals are immutable (type `&str`). See the section `String Literals`
above for more info.

We can use `String` which exists on the heap. We can create them from a string
literal and modify it.

```rs
fn main() {
    let mut s = String::from("hello");
    
    // append something to it with push_str
    s.push_str(", world!");
    
    // we cannot do this because it's not a string literal.
    // println!(s); // Compiler error

    // print it
    println!("{}", s); // hello, world!
}
```

## Move
When the value leaves the scope, Rust automatically calls `drop` at the closing
curly braces. A String has three parts:

1. ptr: Pointer to the memory with the values.
2. len: Number of bytes used by the String.
3. cap: Total number of bytes of memory assigned to the String by the allocator.

Let's create a String and then assign it to another variable like this:

```rs
let s1 = String::from("hello");
let s2 = s1;
```

The `ptr` in both s1 and s2 will point to the same location on the heap with the
value of the string. The value is not copied for s2.

When both s1 and s2 go out of scope we might have gotten a double-free bug
because both wanted to free the memory. To prevent this issue, Rust makes s1
invalid as soon as the assignment happens (`let s2 = s1;`). We cannot use s1
after that.

```rs
fn main() {
    // create a String.
    let s1 = String::from("hello");
    // assign it to s2
    let s2 = s1;
    // try to use s1.
    println!("{}", s1);
    // use s2 so we don't get an "unused variable warning"
    println!("{}", s2);
}
```

And we get an error because s1 was moved.

```
error[E0382]: borrow of moved value: `s1`
 --> src/main.rs:7:20
  |
3 |     let s1 = String::from("hello");
  |         -- move occurs because `s1` has type `String`, which does not implement the `Copy` trait
4 |     // assign it to s2
5 |     let s2 = s1;
  |              -- value moved here
6 |     // try to use s1.
7 |     println!("{}", s1);
  |                    ^^ value borrowed here after move
```

## Clone
But what if we want to make a copy? We use `clone`.

```rs
fn main() {
    // create a String.
    let s1 = String::from("hello");
    // clone it
    let s2 = s1.clone();
    // try to use s1
    println!("{}", s1); // hello
    // use s2 so we don't get an "unused variable warning"
    println!("{}", s2); // hello
}
```

## Copy
But we have seen assignments in other types and both work.

```rs
fn main() {
    let x = 5;
    let y = x;
    
    // we can use both x and y.
    println!("x = {}, y = {}", x, y); // x = 5, y = 5
}
```

These types have a known size at compile time and are stored on the stack. So
assignment here creates a new copy of the entire object on the stack.

If a type has the `Copy` trait, this behavior occurs: Integers, floats, chars,
bools, and Tuples if the types in it have all implemented the `Copy` trait.

## Ownership and Functions
Passing a value to a function will move or copy a value like an assignment.

```rs
// ch04/func_string.rs
fn main() {
    // create a string
    let s = String::from("hello"); 

    // pass it to a function
    use_string(s);

    // we cannot use s here anymore because it was moved to `some_string` and
    // it went out of scope when `use_string` returned.
    println!("{}", s);
}

fn use_string(some_string: String) {
    println!("{}", some_string);
    // some_string goes out of scope. drop is called. Memory is freed.
}
```

We get an error because `s` was moved when passed to the function.

```
error[E0382]: borrow of moved value: `s`
  --> src/main.rs:10:20
   |
3  |     let s = String::from("hello"); 
   |         - move occurs because `s` has type `String`, which does not implement the `Copy` trait
...
6  |     use_string(s);
   |                - value moved here
...
10 |     println!("{}", s);
   |                    ^ value borrowed here after move
```

But we won't have this issue if the type implements the `Copy` trait (e.g., int).

```rs
// ch04/func_int.rs
fn main() {
    // create an int
    let x = 5;

    // x does not move because i32 implements `Copy`.
    use_int(x); // 5
                
    // we can still use x here.
    println!("{}", x);  // 5
}

fn use_int(some_integer: i32) {
    println!("{}", some_integer);
} // some_integer goes out of scope. Nothing special happens.
```

Same thing happens with returns. If we pass a String to a function, we need to
return it from the function to be able to use it later.

## References
To avoid this whole mess of moving when passing variables to function we can use
references. A reference refers to the variable but does not own it. So when we
pass a reference to the function there will be no moves.

`We call the action of creating a reference borrowing.`

```rs
fn main() {
    // create a string
    let s1 = String::from("hello");
    // pass it as a reference to calculate_length
    let len = calculate_length(&s1);
    // we can still use s1 here.
    println!("The length of '{}' is {}.", s1, len);
    // The length of 'hello' is 5.
}

// note the annotation here, the param type is &String
fn calculate_length(s: &String) -> usize {
    return s.len();
    // `s.len()` would do the same
}
```

When `s` goes out of scope at the end of the function, the value for `s1` is not
dropped because `s` does not own it.

We cannot modify `s` inside.

```rs
fn main() {
    // create a string
    let s1 = String::from("hello");
    // pass it as a reference
    modify_s(&s1);
}

fn modify_s(s: &String) {
    s.push_str(" yolo!");
}
```

We get an error.

```
error[E0596]: cannot borrow `*s` as mutable, as it is behind a `&` reference
 --> src/main.rs:9:5
  |
8 | fn modify_s(s: &String) {
  |                ------- help: consider changing this to be a mutable reference: `&mut String`
9 |     s.push_str(" yolo!");
  |     ^^^^^^^^^^^^^^^^^^^^ `s` is a `&` reference, so the data it refers to cannot be borrowed as mutable
```

Let's use the suggestion and pass a mutable reference to the function.

```rs
fn main() {
    // create a string
    let s1 = String::from("hello");
    // pass it as a reference
    modify_mut_s(&mut s1);
}

fn modify_mut_s(s: &mut String) {
    s.push_str(" yolo!");
}
```

We get another error because `s1` is not mutable we cannot borrow it as mutable.

```
error[E0596]: cannot borrow `s1` as mutable, as it is not declared as mutable
 --> src/main.rs:5:18
  |
3 |     let s1 = String::from("hello");
  |         -- help: consider changing this to be mutable: `mut s1`
4 |     // pass it as a reference
5 |     modify_mut_s(&mut s1);
  |                  ^^^^^^^ cannot borrow as mutable
```

Let's make `s1` mutable, too.

```rs
fn main() {
    // create a mutable string
    let mut s1 = String::from("hello");
    // pass it as a mutable reference
    modify_mut_s(&mut s1);
    
    println!("{}", s1); // hello yolo!
}

fn modify_mut_s(s: &mut String) {
    s.push_str(" yolo!");
}
```

And this works! Remember that although `s1` is mutable, we could have borrowed
it as immutable.

## Mutable References
We can only have one mutable reference to a value at a time. This code won't
work:

```rs
fn main() {
    // create a mutable string
    let mut s1 = String::from("hello");
    
    let r1 = &mut s1;
    let r2 = &mut s1;

    println!("{}, {}", r1, r2);
}
```

We get this error:

```
error[E0499]: cannot borrow `s1` as mutable more than once at a time
 --> src/main.rs:6:14
  |
5 |     let r1 = &mut s1;
  |              ------- first mutable borrow occurs here
6 |     let r2 = &mut s1;
  |              ^^^^^^^ second mutable borrow occurs here
7 | 
8 |     println!("{}, {}", r1, r2);
  |                        -- first borrow later used here
```

This supposedly helps with data races.

We cannot also have mutable and immutable borrows at the same time.

```rs
fn main() {
    let mut s = String::from("hello");

    let r1 = &s; // no problem
    let r2 = &s; // no problem
    let r3 = &mut s; // BIG PROBLEM

    println!("{}, {}, and {}", r1, r2, r3);
}
```

Because we have an immutable reference in the same scope. Multiple immutable
references are allowed.

```
error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
 --> src/main.rs:6:14
  |
4 |     let r1 = &s; // no problem
  |              -- immutable borrow occurs here
5 |     let r2 = &s; // no problem
6 |     let r3 = &mut s; // BIG PROBLEM
  |              ^^^^^^ mutable borrow occurs here
7 | 
8 |     println!("{}, {}, and {}", r1, r2, r3);
  |                                -- immutable borrow later used here
```

## Reference Scope
The scope of a reference starts from where it's introduced until the last time
it is used even though the block has not finished. It's a bit different from
variable references. E.g., this will work because r1 and r2 are not used after
r3 is created.

```rs
fn main() {
    let mut s = String::from("hello");

    let r1 = &s; // no problem
    let r2 = &s; // no problem
    println!("{} and {}", r1, r2);
    // variables r1 and r2 will not be used after this point

    let r3 = &mut s; // no problem
    println!("{}", r3);
}
```

## Dangling Reference
The compiler does not allow us to create dangling references. This won't work:

```rs
fn main() {
    let reference_to_nothing = dangle();
}

fn dangle() -> &String {
    let s = String::from("hello");

    &s
}
```

`dangle` creates s and wants to return a reference to it. However, after dangle
returns, s goes out of scope and is deallocated. Hence, a dangling reference.
The compiler returns an error. Instead, we can return the `s`.

```
this function's return type contains a borrowed value, but there is no value for
it to be borrowed from help: consider using the `'static` lifetime
```

## The Slice Type
Similar to slice in Go? You can reference a sequence in a collection without
ownership.

Small function to find the index of the first word in a string.

```rs
fn first_word(s: &String) -> usize {
    // converts the string to an array of bytes
    let bytes = s.as_bytes();

    // bytes.iter.enumerate() returns a tuple. The index and a reference to the item
    // here we are destructuring the tuple
    for (i, &item) in bytes.iter().enumerate() {
        // compare the character with space
        if item == b' ' {
            return i;
        }
    }

    // if there's no space in the string, all of it is the word
    s.len()
}
```

However, this is not useful because it's an index to a string that might have
been modified since then. Instead, we can return a String slice with the words.

## String Slice
Create it like this. Note the second index is exclusive. E.g., `[0..5]` starts
from index 0 and ends at 4.

```rs
fn main() {
    let s = String::from("hello world");

    let hello = &s[0..5];
    let world = &s[6..11];

    println!("{} - {}", hello, world);
}
```

We can drop the lower range if we want to start from the beginning. So `[0..5]`
and `[..5]` are the same.

If the higher range is the end we can drop it. E.g., `[4..]` goes from index 4
to the end.

`[..]` creates a slice from the whole string. `let slice = &s[..]`. Now, we can
rewrite the function to return a slice.

```rs
fn first_word(s: &String) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}
```

**String literals are slices.** Remember what we saw in the string literal
section? Their type is `&str`.

## Other Slices
We can create slices of other types.

```rs
fn main() {

    let a = [1, 2, 3, 4, 5];
    let slice = &a[1..3];
    
    println!("{:?}", slice);    // [2, 3]
}
```

# Chapter 5

## Structs
Similar to other programming languages.

```rs
// ch05/basic_struct.rs
// define a struct
struct Game {
        name: String,
        hours_played: u32,
        path: String,
}

fn main() {

    // create a mutable object
    let mut game1 = Game {
        name: String::from("Windows Calculator"),
        hours_played: 123,
        path: String::from("C:/Windows/System32/calc.exe"),
    };
    
    // access fields
    println!("{}, {}, {}", game1.name, game1.hours_played, game1.path);
    // Windows Calculator, 123, C:/Windows/System32/calc.exe
    
    // change fields
    game1.path = String::from("C:\\Windows\\System32\\calc.exe");
    // print the modified field
    println!("{}", game1.path);
    // C:\Windows\System32\calc.exe
}
```

We cannot set specific fields to mutable. Whole object needs to be mutable or
not.

## Field Init Shorthand
Let's say we have this function to create a new `Game` object.

```rs
fn build_game(name: String, hours_played: u32, path: String) -> Game {
    Game {
        name: name,
        hours_played: hours_played,
        path: path,
    }

    // apparently using the return keyword is _bad_.
}
```

If the name of the field and the variable with the value is the same like the
above we can do a shorthand like this.

```rs
// complete example in ch05/field_init_shorthand.rs
fn build_game(name: String, hours_played: u32, path: String) -> Game {
    Game {
        name,
        hours_played,
        path,
    }
}
```

## Struct Update Syntax
We can create a new object with the values from a previous object and only
modify some.

```rs
// complete example in ch05/struct_update.rs

fn main() {

    // create a game object
    let game1 = Game {
        name: String::from("Windows Calculator"),
        hours_played: 123,
        path: String::from("C:/Windows/System32/calc.exe"),
    };
    
    // create game2 based on game1 with a new path
    let game2 = Game {
        path: String::from("C:\\Windows\\System32\\calc.exe"),
        ..game1
    };
    
    // access fields
    println!("{}, {}, {}", game2.name, game2.hours_played, game2.path);
    // Windows Calculator, 123, C:\Windows\System32\calc.exe
}
```

**However, we moved game1 so we cannot use it anymore.** Because we used the
value of `String` for the `name` field. If we had only copied the fixed-length
values of `game1` then we would have been able to use it. Here's an example to
show that.

Note how `print_game` accepts a reference, if we had passed the
actual object it would have been moved after calling the function and we could
not have used it anymore.

```rs
// ch05/struct_update_move.rs
// define a struct
struct Game {
    name: String,
    hours_played: u32,
    path: String,
}

fn print_game(game: &Game) {
    println!("{}, {}, {}", game.name, game.hours_played, game.path);
}

fn main() {

    // create a game object
    let game1 = Game {
        name: String::from("Windows Calculator"),
        hours_played: 123,
        path: String::from("C:/Windows/System32/calc.exe"),
    };
    
    // create game1_new based on game1 but only reuse hours_played which is the
    // only fixed-length field
    let game1_new = Game {
        name: String::from("Guild Wars"),
        path: String::from("C:/Guild Wars/gw.exe"),
        ..game1
    };
    
    // we can still use game1 here because we did not "move" any of the Strings
    // create game2 based on game1 with a new path
    print_game(&game1);
    // Windows Calculator, 123, C:/Windows/System32/calc.exe
    
    print_game(&game1_new);
    // Guild Wars, 123, C:/Guild Wars/gw.exe
    
    // create game2_new but reuse the Strings so they are "moved"
    let game1_new_new = Game {
        hours_played: 6000,
        ..game1
    };
    
    // we cannot use game1 anymore.
    print_game(&game1);  // <-- error here
    print_game(&game1_new_new);
}
```

We get an error in the last `print_game(&game1)` because `game1` was partially
moved when creating `game1_new_new`.

```
error[E0382]: borrow of partially moved value: `game1`
  --> src/main.rs:44:16
   |
38 |       let game1_new_new = Game {
   |  _________________________-
39 | |         hours_played: 6000,
40 | |         ..game1
41 | |     };
   | |_____- value partially moved here
...
44 |       print_game(&game1);  // <-- error here
   |                  ^^^^^^ value borrowed here after partial move
   |
   = note: partial move occurs because `game1.path` has type `String`, which does not implement the `Copy` trait
```

## Tuple Structs
Think of them as structs but without field names. We can access the fields by
index (see in `print_game`).

```rs
// ch05/tuple_struct.rs

// define two tuple structs
struct Game(String, u32, String);
struct App(String, u32, String);

fn print_game(game: &Game) {
    // we can access the tuple struct's fields with the index
    println!("{}, {}, {}", game.0, game.1, game.2);
}

fn main() {

    let game1 = Game(
        String::from("Guild Wars"),
        5000,
        String::from("C:/Guild Wars/gw.exe")
    );
    
    print_game(&game1);
    // Guild Wars, 5000, C:/Guild Wars/gw.exe
    
    let app1 = App(
        String::from("Windows Calculator"),
        123,
        String::from("C:/Windows/System32/Calc.exe")
    );
    
    // we cannot call print_game with &App because they are different structs
    // although they have the same fields
    print_game(&app1);  // <-- error 'expected struct `Game`, found struct `App`'
}
```

`Game` and `App` are different structs although they have similar fields.

## Unit-Like Structs
They don't have any fields.

```rs
struct Whatever;

let wt = Whatever;
```

## Derived Traits
We cannot use `println!` to print the `Game` struct.

```rs
struct Game {
    name: String,
    hours_played: u32,
    path: String,
}

fn main() {

    let game1 = Game {
        name: String::from("Guild Wars"),
        hours_played: 5000,
        path: String::from("C:/Guild Wars/gw.exe")
    };
    
    println!("{}", game1);
}
```

We get an error in `println!` because it does not implement the
`std::fmt::Display` trait.

```
error[E0277]: `Game` doesn't implement `std::fmt::Display`
  --> src/main.rs:15:20
   |
15 |     println!("{}", game1);
   |                    ^^^^^ `Game` cannot be formatted with the default formatter
   |
   = help: the trait `std::fmt::Display` is not implemented for `Game`
   = note: in format strings you may be able to use `{:?}` (or {:#?} for pretty-print) instead
```

The error tells us we can use `println!("{:?}", game1);` which results in
another error:

```
error[E0277]: `Game` doesn't implement `Debug`
  --> src/main.rs:15:22
   |
15 |     println!("{:?}", game1);
   |                      ^^^^^ `Game` cannot be formatted using `{:?}`
   |
   = help: the trait `Debug` is not implemented for `Game`
   = note: add `#[derive(Debug)]` to `Game` or manually `impl Debug for Game`
   = note: this error originates in the macro `$crate::format_args_nl` (in Nightly builds, run with -Z macro-backtrace for more info)
```

Let's add `#[derive(Debug)]` to `Game`.

```rs
#[derive(Debug)]
struct Game {
    name: String,
    hours_played: u32,
    path: String,
}

fn main() {

    let game1 = Game {
        name: String::from("Guild Wars"),
        hours_played: 5000,
        path: String::from("C:/Guild Wars/gw.exe")
    };
    
    println!("{:?}", game1);
}
```

Finally:
`Game { name: "Guild Wars", hours_played: 5000, path: "C:/Guild Wars/gw.exe" }`.

## The dbg Macro
We can use the `dbg!` macro to print to `stderr` (`println!` prints to
`stdout`). It prints info about the parameter and returns their ownership. We
can also pass references to it.

```rs
#[derive(Debug)]
struct Game {
    name: String,
    hours_played: u32,
    path: String,
}

fn main() {

    let game1 = Game {
        name: String::from("Guild Wars"),
        hours_played: dbg!(5000),
        path: String::from("C:/Guild Wars/gw.exe")
    };
    
    dbg!(&game1);
}
```

The result:

```
[src/main.rs:12] 5000 = 5000
[src/main.rs:16] &game1 = Game {
    name: "Guild Wars",
    hours_played: 5000,
    path: "C:/Guild Wars/gw.exe",
}
```

## Methods
We can convert `print_game` into a method that we can call on `Game` objects.
They are defined similar to normal functions, but their first param is always
`self`.

```rs
// ch05/method1.rs
struct Game {
    name: String,
    hours_played: u32,
    path: String,
}

impl Game {
    // implement print for Game
    fn print(&self) {
        println!("{}, {}, {}", self.name, self.hours_played, self.path);
    }
}

fn main() {

    let game1 = Game {
        name: String::from("Guild Wars"),
        hours_played: 5000,
        path: String::from("C:/Guild Wars/gw.exe"),
    };
    
    game1.print();
    // Guild Wars, 5000, C:/Guild Wars/gw.exe
}
```

Note how we are passing `&self` to `print`. Methods can also take ownership of
`self` and other parameters.

We can name a method the same as a field. Usually, these are getters and return
the value of the field.

```rs
impl Game {
    fn name(&self) -> String {
        self.name
    }
}
```

Now, we can call `game1.name()` to get the value of `name`.

## Automatic Referencing and Dereferencing
When calling methods, Rust automatically add `&`, `&mut`, or `*` to the object
to match the method signature. Hence, why we did not do `(&game1).print()`
although the receiver was `&self`.

## Associated Functions
Functions inside an `impl` block are called `associated functions` because they
are associated with a struct.

We can define non-method associated functions (they do not have the `&self`
param). Let's add a function that creates a game object for calc.

```rs
// ch05/associated_method_calc.rs
struct Game {
    name: String,
    hours_played: u32,
    path: String,
}

impl Game {

    fn print(&self) {
        println!("{}, {}, {}", self.name, self.hours_played, self.path);
    }

    fn calc() -> Game {
        Game {
            name: String::from("Windows Calculator"),
            hours_played: 0,
            path: String::from("C:/Windows/System32/calc.exe"),
        }
    }
}

fn main() {
    let calc = Game::calc();
    calc.print();
    // Windows Calculator, 0, C:/Windows/System32/calc.exe
}
```

We can call it with `Game::calc()` similar to `String::from(...)`.

**We can have multiple impl blocks**.

# Chapter 6

## Define an Enum
We can create an enum:

```rs
enum AppType {
    Utility,
    Game,
}

// get an enum
let util = AppType::Utility;
```

We can define functions that take a param of type `AppType`. Revamping the
game example from before:

```rs
// ch06/enum1.rs

// needed to print the AppType values
#[derive(Debug)]
enum AppType {
    Utility,
    Game,
} 

struct App {
    name: String,
    hours_played: u32,
    path: String,
    app_type: AppType,
}

impl App {

    fn print(&self) {
        println!(
            "Name: {}, Hours played: {}, Path: {}, Type: {:?}",
            self.name,
            self.hours_played,
            self.path,
            self.app_type
        );
    }
}

fn main() {

    let calc = App {
        name: String::from("Windows Calculator"),
        hours_played: 123,
        path: String::from("C:/Windows/System32/calc.exe"),
        app_type: AppType::Utility,
    };

    calc.print();
    // Name: Windows Calculator, Hours played: 123, Path: C:/Windows/System32/calc.exe, Type: Utility
}
```

Note how I have used `#[derive(Debug)]` before the enum to print its value with
`{:?}`. Otherwise it does not work.

We can also ditch the struct and do everything in the enum.

```rs
// ch06/enum2.rs
#[derive(Debug)]
enum AppType {
    // name and path.
    Utility(String, String),
    // name, path, hours_played
    Game(String, String, u32),
}

fn main() {
    let calc = AppType::Utility(
        String::from("Windows Calculator"),
        String::from("C:/Windows/System32/calc.exe"),
    );

    let gw = AppType::Game(
        String::from("Guild Wars"),
        String::from("C:/Guild Wars/gw.exe"),
        5000,
    );

    println!("{:?}", calc);
    // Utility("Windows Calculator", "C:/Windows/System32/calc.exe")
    
    println!("{:?}", gw);
    // Game("Guild Wars", "C:/Guild Wars/gw.exe", 5000)
}
```

We can also define structs and pass them as a parameter to the enum function.

```rs
// ch06/enum3.rs
#[derive(Debug)]
struct GameStruct {
    name: String,
    path: String,
    hours_played: u32,
}

#[derive(Debug)]
struct UtilStruct {
    name: String,
    path: String,
}

#[derive(Debug)]
enum AppType {
    Game(GameStruct),
    Utility(UtilStruct),
}

fn main() {
    let calc = AppType::Utility(UtilStruct {
        name: String::from("Windows Calculator"),
        path: String::from("C:/Windows/System32/calc.exe"),
    });
    
    println!("{:?}", calc);
    // Utility(UtilStruct { name: "Windows Calculator", path: "C:/Windows/System32/calc.exe" })
}
```

We can have different things in the enum like the example from the book:

```rs
enum Message {
    // no data associated with it.
    Quit,
    // named fields like a struct
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
```

## Enum Methods and match
We can also have enum methods. Let's define the new `print` method that returns
a String that represents each enum.

```rs
// ch06/enum4.rs
enum AppType {
    Game(GameStruct),
    Utility(UtilStruct),
}

impl AppType {
    fn stringer(&self) -> String {
        match self {
            AppType::Game(g) => format!(
                "Name: {}, Path: {}, Hours Played: {}",
                g.name, g.path, g.hours_played
            ),
            AppType::Utility(u) => format!("Name: {}, Path: {}", u.name, u.path),
        }
    }
}
```

Note how we are using `match` and are able to access the enum parameters (in
this case structs). The `format!` macro returns a formatted `String`.

## Option Enum
Rust does not have null but the `Option` enum allows us to have `None`.

```rs
enum Option<T> {
    None,
    Some(T),
}
```

We can use `Some` and `None` directly without importing anything.
`<T> == lol yes generics`.

```rs
// Option<i32>
let some_number = Some(5);
let absent_number: Option<i32> = None;  // we have to enter the type for None

// Option<&str>
let some_string = Some("a string");
```

## Matching with Option<T>
We can try to write a function that extracts the value of `u32` from
`Option<i32>` like this:

```rs
fn extract_option(o: Option<u32>) -> u32 {
    match o {
        Some(i) => i,
    }
}
```

This returns `i` for `Some(i)`, but the compiler complains about not handling
`None`.

```
error[E0004]: non-exhaustive patterns: `None` not covered
   --> src/main.rs:2:11
    |
2   |     match o {
    |           ^ pattern `None` not covered
    |
```

Basically, the match should cover all possible values. They are **exhaustive**.
Here, we will have a dilemma. What should we return as `None`? `None` is the
absence of values here. A very naive way would be returning 0. But that means
`Some(0)` and `None` would be the same.

```rs
fn extract_option(o: Option<u32>) -> u32 {
    match o {
        Some(i) => i,
        None => 0,
    }
}

fn main() {
    let s1 = Some(0);
    let n1: Option<u32> = None;
    
    println!("{}", extract_option(s1)); // 0
    println!("{}", extract_option(n1)); // 0
}
```

I still don't know how to use `None`, but let's move on.

Writing exhaustive matches will be boring if we only want to take action for a
few values. This is why we have `other`. So, we can write matches like this.

```rs
match user_input {
    1 => {
        do1();
        launch();
    } // we can have a block here, too - rustfmt removes the colon here
    2 => abort(),
    other => try_again(other), // note how we can use `other` in the arm
}
```

If we don't want to use the value, we can use `_` instead of `other`.

```rs
match user_input {
    1 => {
        do1();
        launch();
    }
    2 => abort(),
    _ => try_again(), // run try_again for all other values
}
```

If we really don't want to do anything, we can replace `try_again()` with `()`:

```rs
match user_input {
    1 => {
        do1();
        launch();
    }
    2 => abort(),
    _ => (), // don't do anything for all other values
}
```

## if let
Well, this is very confusing!

Similar to a `match` but not exhaustive. These two are supposedly the same.

```rs
let config_max = Some(3);
match config_max {
    Some(max) => println!("The maximum is configured to be {}", max),
    _ => (),
}
```

Because of the `let`, the value of `max` will be `3u8` after the `if`.

```rs
let config_max = Some(3);
if let Some(max) = config_max {
    println!("The maximum is configured to be {}", max);
}
```

This gets more confusing because if we already have a `max` variable, it will be
shadowed here.

```rs
fn main() {
    let config_max = Some(3);
    let max = 10;
    println!("{}", max); // prints "10"

    if let Some(max) = config_max {
        println!("{}", max); // prints "3"
    }
    println!("{}", max); // prints "10"
}
```

I should stop thinking of this as an `if`. Not sure how I can handle using it
later when writing Rust. We can also have `else` here which is like the `_` in
match and matches everything else.

```rs
fn main() {
    let config_max = Some(3);
    if let Some(max) = config_max {
        println!("{}", max); // prints "3"
    } else {
        println!("{}", "not 3");
    }
}
```

# Chapter 7

## Packages & Crates

* Crate: A binary of library.
* Crate root: The source file the compiler starts from.
    * `src/main.rs`: Crate root of binary crate with the same name as the package.
        * More binary crates will be in `src/bin`.
    * `src/lib.rs`: Crate root of library crate with the same name as the package. 
* Package: One or more crates.
    * Has `Cargo.toml` which describes how to build the crates.
    * Has at most one library crate and many binary crates.
    * Must have at least one crate.

## Modules
Modules help us organize code within a crate into groups. Also `public/private`
items. Defined with the `mod` keyword. Modules can be nested, too.

```rs
mod applications {
    mod games {
        fn start() {}
    }
    mod utilities {
        fn start_utility() {}
    }
}
```

`games` and `utilities` are sibling modules. They are defined in the same module
and have the same parent. All top level modules are children of an implicit
module named `crate`. In this code `applications` is a child of `crate`.

## Paths
How to tell Rust where to find an item in the module tree. Separator is `::`.

* Absolute: Starts with the create name or `crate`.
* Relative: Starts from the current module and uses `self`, `super`, or an
  identifier in the current module.

```rs
// ch07/restaurant/src/lib.rs
mod applications {
    mod games {
        fn start() {}
    }
    mod utilities {
        fn start_utility() {}
    }
}

// pub makes it public, more about it later
pub fn run_game() {
    // absolute path
    crate::applications::games::start();

    // relative path
    applications::games::start();
}
```

`applications` is defined in the same level as run_game so we can start with it
in a relative path.

We cannot build this with `cargo build` because the `games` module is private.

```
error[E0603]: module `games` is private
  --> src/lib.rs:13:26
   |
13 |     crate::applications::games::start();
   |                          ^^^^^ private module
   |
note: the module `games` is defined here
  --> src/lib.rs:2:5
   |
2  |     mod games {
   |     ^^^^^^^^^
```

## Rust's Privacy Boundary
Everything is private by default in Rust. We have to use `pub` to make them
public.

Parent modules cannot see items in their child modules, but child
modules can use items in their parent modules.

If we just make the `games` module public (`pub mod games`) we still get an
error becuse `start` is still private. It must be public, too.

```rs
mod applications {
    pub mod games {
        pub fn start() {}
    }
    mod utilities {
        fn start_utility() {}
    }
}

// now this works
// crate::applications::games::start();
```

Why can we call stuff in the `applications` module although it's not public?
Because `run_game()` is defined in the same module.

## Super
Equal to `..` in the file system. We can refer to parent modules. `delete_stuff`
is defined in `applications`. We can call it `super` from inside `games`.

```rs
mod applications {
    pub mod games {
        pub fn start() {}

        fn delete() {
            // call delete_stuff() from `applications`
            super::delete_stuff();
        }
    }
    mod utilities {
        fn start_utility() {}
    }

    fn delete_stuff() {}
}
```

## Public Structs
We can make structs public with `pub` but the fields will stay private unless we
manually make them public, too.

```rs
// ch07/applications/src/lib.rs
mod applications {
    pub mod games {
        // public struct
        pub struct Game {
            pub name: String,   // public field
            hours_played: u32,  // private field
        }
    }
}

pub fn create_guild_wars() -> Game {
    applications::games::Game {
        name: String::from("Guild Wars"),
        hours_played: 5000,  // error here because the field is private
    }
}
```

We cannot access `hours_played` inside because it's a private field.

```
error[E0451]: field `hours_played` of struct `Game` is private
  --> src/lib.rs:14:9
   |
14 |         hours_played: 123,
   |         ^^^^^^^^^^^^^^^^^ private field
```

If we want to keep the field private, we need to create getters and setters for
it. Another solution is moving the `create_calc()` function to the `games`
module. It will be adjacent to the `Game` struct and can use its fields. This
will work even if `Game` is not public but we probably want to use it outside of
the module in other parts of the program.

```rs
mod applications {
    pub mod games {
        // public struct
        pub struct Game {
            name: String,
            hours_played: u32,
        }
        pub fn create_guild_wars() -> Game {
            Game {
                name: String::from("Guild Wars"),
                hours_played: 5000,
            }
        }
    }
}
```

## Public Enums
Making an enum public will make all its variants public, too. We can use
`Utility` and `Game` because `AppType` is public.

```rs
// ch07/enums/src/lib.rs
mod applications {

    pub mod app_enums {
        // public enum
        pub enum AppType {
            Utility,
            Game,
        }
    }
}

fn create_enums() {
    let calc = applications::app_enums::AppType::Utility;
    let gw = applications::app_enums::AppType::Game;
}
```

## The use Keyword
We can bring paths into our scope with `use`. We don't have to write the
complete path. We can use both absolute and relative paths.

```rs
mod applications {
    pub mod app_enums {
        // public enum
        pub enum AppType {
            Utility,
            Game,
        }
    }
}

// absolute path
// use crate::applications::app_enums::AppType;

// can also use relative paths
// use applications::app_enums::AppType;
// or use self in the relative path
use self::applications::app_enums::AppType;

fn create_enums() {
    let calc = AppType::Utility;
    let gw = AppType::Game;
}
```

Note how we can use `self` in the relative path. The book uses `self` but
removing it did not cause an issue for me.

We can also bring `Utility` and `Game` directly to scope, but that is not
recommended. By using `AppType` we show they are not locally defined and it
helps us discover where they are defined.

```rs
// this works but not recommended
use applications::app_enums::AppType::Utility;
use applications::app_enums::AppType::Game;

fn create_enums() {
    let calc = Utility;
    let gw = Game;
}
```

> when bringing in structs, enums, and other items with use, it’s idiomatic to
> specify the full path.

If there are two items with the same name then we can `use` the parents.

Or we can use the `as` keyword to bring an item to the current scope with a
different name. Doesn't make sense here, but good for demonstration.

```rs
use applications::app_enums::AppType as ApplicationType;

fn create_enums() {
    let calc = ApplicationType::Utility;
    let gw = ApplicationType::Game;
}
```

## pub use
Items brought into the current scope are private to external code. E.g., we have
`Config` struct imported and we want code that uses are our module to be able to
access it.

```rs
pub use configs::Config;

fn use_config(c: Config) {
    // do something
}
```

## Nested Paths in use
If we are using items from the same path.

```rs
mod applications {
    pub mod games {
        fn start() {}
    }
    pub mod utilities {
        fn start_utility() {}
    }
}

use applications::{games, utilities};
```

We can also use the glob operator `*` to import everything public under a path.
Useful in tests but not anywhere else: `use std::collections::*;`.

## Modules in Different Files
We're gonna refactor our `applications` crate in the
`applications_separate_files` crate.

```rs
// ch07/applications_separate_files/lib.rs

// declare the `applications` module, content will be in `applications.rs`.
mod applications;

use applications::games::{create_guild_wars, Game};

fn create_gw() -> Game {
    // do something
    create_guild_wars()
}
```

`mod applications;` in the file tells Rust to look for the contents of this
module in `applications.rs` (in the same file path).

```rs
// ch07/applications_separate_files/applications.rs
pub mod games {
    // removed
}

pub mod utilities {
    // removed
}
```

We could also move `games` and `utilities` into their own files.

```rs
// ch07/applications_separate_files/applications.rs
pub mod games;

pub mod utilities;
```

Then put the code in `applications/games.rs` and `applications/utilities.rs`
respectively. Note they will be inside the `applications` directory.

```
.
├── Cargo.lock
├── Cargo.toml
└── src
    ├── applications
    │   ├── games.rs
    │   └── utilities.rs
    ├── applications.rs
    └── lib.rs
```

# Chapter 8

## Vectors
`Vev<T>` or vectors. Store values of the same type sequentially in memory. All
vector elements are destroyed when vector goes out of scope.

```rs
// empty vector of u32 values
let mut v: Vec<u32> = Vec::new();
// add values with push
v.push(1);
v.push(2);

// Rust can infer the type with the vec! macro, it will be i32 here
let v2 = vec![1, 2, 3];
```

## Read Vector Values
There are two ways to read vector elements.

1. Index
2. `.get`

Index starts from zero and is similar to other languages.

```rs
fn main() {
    let mut v: Vec<u32> = Vec::new();
 
    v.push(0);
    v.push(1);
    
    let nem = v[1];
    println!("nem = {}", nem);      // 1
    println!("v[1] = {}", v[1]);    // 1
    let bem = &v[1];
    println!("^v[1] = {}", nem);    // 1
}
```

Using `let nem = v[1];` is not really a good thing. We are looking at u32 which
is a fixed-length type and hence it's not moved. Let's try with strings.

```rs
fn main() {
    let mut v: Vec<String> = Vec::new();
 
    v.push(String::from("0"));
    v.push(String::from("1"));
    
    let nem = v[1];             // error here
    println!("nem = {}", nem);
    println!("v[1] = {}", v[1]);
    let bem = &v[1];
    println!("^v[1] = {}", nem);
}
```

We get an error because we cannot move and index of a vector (`v[1]` in this
case).

```
error[E0507]: cannot move out of index of `Vec<String>`
  --> src/main.rs:11:15
   |
11 |     let nem = v[1];
   |               ^^^^
   |               |
   |               move occurs because value has type `String`, which does not implement the `Copy` trait
   |               help: consider borrowing here: `&v[1]`
```

Instead we must borrow it.

```rs
fn main() {
    let mut v: Vec<String> = Vec::new();
 
    v.push(String::from("0"));
    v.push(String::from("1"));
    
    let nem = &v[1];    // borrow instead of move
    println!("nem = {}", nem);      // nem = 1
    println!("v[1] = {}", v[1]);    // v[1] = 1
    let bem = &v[1];
    println!("^v[1] = {}", nem);    // ^v[1] = 1
}
```

With the `get` method we receive an `Option<T>` (`Option<String>` here).

```rs
fn main() {
    let mut v: Vec<String> = Vec::new();
 
    v.push(String::from("0"));
    v.push(String::from("1"));
    
    let index = 0;
    let v0 = v.get(index);
    match v0 {
        Some(value) => println!("v[{}] = {}", index, value),    // v[0] = 0
        None => println!("v[{}] = None", index),
    }
}
```

This method is usually better because it returns `None` if the index is out of
range. We can catch it. E.g., changing `index` to 10 gives us:

```rs
fn main() {
    let mut v: Vec<String> = Vec::new();
 
    v.push(String::from("0"));
    v.push(String::from("1"));
    
    let index = 10;
    let v0 = v.get(index);
    match v0 {
        Some(value) => println!("v[{}] = {}", index, value),
        None => println!("v[{}] = None", index),    // v[10] = None
    }
}
```

However, `v[10]` using the index will panic.

```rs
fn main() {
    let mut v: Vec<String> = Vec::new();
 
    v.push(String::from("0"));
    v.push(String::from("1"));
    
    let index = 10;
    println!("v[{}] = {}", index, v[index]);
    // thread 'main' panicked at 'index out of bounds: the len is 2 but the
    // index is 10', src/main.rs:8:35
}
```

**We cannot have both mutable and immutable references to even different
elements of the vector**.

```rs
fn main() {
    let mut v: Vec<String> = Vec::new();
 
    v.push(String::from("0"));
    v.push(String::from("1"));
    
    let immutable_ref = v.get(0);
    
    // add something to the vector
    v.push(String::from("2"));
    
    // use the immutable reference <-- error
    match immutable_ref {
        Some(val) => println!("{}", val),
        None => (),
    }
}
```

We will get an error when we use `immutable_ref` after modifying the vector.
Even though our reference is to a specific element. We cannot modify the vector
if we have an immutable reference to any of its elements. Because we might have
to allocate more memory so the vector is moved in memory and the reference to
element is not valid anymore.

```
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
  --> src/main.rs:10:5
   |
7  |     let immutable_ref = v.get(0);
   |                         -------- immutable borrow occurs here
...
10 |     v.push(String::from("2"));
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^ mutable borrow occurs here
...
13 |     match immutable_ref {
   |           ------------- immutable borrow later used here
```

## Iterate over Vector Elements
We can use a `for` loop.

```rs
fn main() {
    let mut v: Vec<String> = Vec::new();
 
    v.push(String::from("0"));
    v.push(String::from("1"));
    
    // modify elements with mutable references
    for s in &mut v {
        (*s).push_str("0");
        
        // s.push_str("0");        
        // also works because of automatic dereferencing
    }
    
    // print all elements
    for s in &v {
        println!("{}", s);  // 00 10
    }
}
```

Because we are iterating over references we need to derefence `s`. However, we
are calling a method on it to modify it so automatic dereferencing means we can
just do `s.push_str(...)` and it will work.

## Using an Enum to Store Multiple Types
Vectors can only store values of the same type, but we can define an enum with
different types and then store values of that enum type in the vector.

This works if we know what types will be added to the vector at compile time.

```rs
enum SpreadsheetCell {
    Int(i32),
    Float(f64),
    Text(String),
}

let row = vec![
    SpreadsheetCell::Int(3),
    SpreadsheetCell::Text(String::from("blue")),
    SpreadsheetCell::Float(10.12),
];
```

## Remove Vector Values
We can remove the last value with `pop` and get an `Option<T>` or `None` if the
vector is empty. 

```rs
fn main() {
    let mut v: Vec<String> = Vec::new();

    v.push(String::from("0"));
    println!("{}", extract_vector_value(v.pop()));  // "0"
    println!("{}", extract_vector_value(v.pop()));  // "None"
}

fn extract_vector_value(s: Option<String>) -> String {
    match s {
        Some(st) => st,
        None => String::from("None"),
    }
}
```

There are more methods. See https://doc.rust-lang.org/std/vec/struct.Vec.html.

## Strings
Mostly talking about `String` in this section. This type is `UTF-8` encoded.

```rs
// create a new String
let mut s1 = String::new();

// convert a string literal to a String
let s1_lit = "Guild Wars";
let s2 = s1_lit.to_string();    // String type

// directly convert a string literal to String
let s3 = "Guild Wars".to_string();
// we've already seen `from`, too
let mut s4 = String::from("Guild Wars");

// append a string literal to a String
s4.push_str(" 2");  // "Guild Wars 2"
// append a single character to a String
s4.push('!');       // "Guild Wars 2!"
```

We can also concat String with `+`. The caveat is that first operand must be a
`String` and second must be `&str` and the result is another `String`. The first
operand will be moved, too.

```rs
fn main() {
    let first = String::from("Guild Wars");
    let second = String::from(" Rocks!");

    println!("{}", first + &second);    // "Guild Wars Rocks!"
    // first has been moved and we cannot use it anymore
}
```

We can also use `&String` because the compiler can coerce it to `&str`. Rust
uses a deref coercion to convert `&second` to `&second[..]`. `second` is not
moved.

> Rust Strings do not support indexing. We cannot do `st[1]`.

> **Don't slice Strings**. Depending on how the String is sliced, the return
> value could be different.

We can iterate over String bytes, but each byte might not be a valid char
depending on the length of each char encoded in UTF-8. E.g., it could be encoded
in 2 bytes and grabbing the first byte does not give us the actual character.

```rs
for c in "whatever".bytes() {
    println!("{}", c);
}
```

It works here because each char in the string above is encoded as one byte in
UTF-8.

## HashMaps
`HashMap<K, V>` maps keys of type `K` to values of type `V`.

```rs
use std::collections::HashMap;

let mut hm = HashMap::new();

// by passing these values the type will be HashMap<String, i32>
hm.insert(String::from("key0"), 0);
hm.insert(String::from("key1"), 1);
```

We can also create a HashMap by using two vectors. One will be key and the other
will be the values.

```rs
use std::collections::HashMap;

let keys = vec![String::from("key0"), String::from("key1")];
let values = vec![0, 1];

let mut hm: HashMap<_, _> = keys.into_iter().zip(values.into_iter()).collect();
```

## HashMaps and Ownership
Variable length values will be moved when they are stored in the HashMap.
HashMaps are also stored on the heap because their size is unknown at compile
time.

## Reading HashMaps
We can read the values with `.get(&key)`. Result is `Option<V>`. `Some(value)`
if the key exists and `None` if it doesn't.

```rs
fn main() {
    use std::collections::HashMap;

    let mut hm = HashMap::new();
    hm.insert(String::from("key0"), 0);
    hm.insert(String::from("key1"), 1);

    let val = hm.get(&String::from("key0"));

    print_option(val);                          // 0
    print_option(hm.get(&String::from("123"))); // "None"
}

fn print_option(o: Option<&i32>) {
    match o {
        Some(val) => println!("{}", val),
        None => println!("None"),
    }
}
```

## Iterating over the HashMap
This is similar to other languages. Be sure to pass a reference to the HashMap
to `for`

```rs
fn main() {
    use std::collections::HashMap;

    let mut hm = HashMap::new();
    hm.insert(String::from("key0"), 0);
    hm.insert(String::from("key1"), 1);

    let val = hm.get(&String::from("key0"));

    for (k, v) in &hm {
        println!("{}: {}", k, v);
    }
}
```

## Updating a Hash Map
Calling `insert` with an existing key will overwrite the value for that key.
Otherwise, it will add the key-value pair.

Check if a key exists and only add it if it does not.

```rs
fn main() {
    use std::collections::HashMap;

    let mut hm = HashMap::new();
    hm.insert(String::from("key0"), 0);

    hm.entry(String::from("key0")).or_insert(-1);
    hm.entry(String::from("key1")).or_insert(1);

    println!("{:?}", hm);   // {"key0": 0, "key1": 1}
}
```

`entry` returns an enum called `Entry`. For an existing key it looks like this:

```rs
let nem = hm.entry(String::from("key0"));
println!({":?}", nem);

// Entry(OccupiedEntry { key: "key0", value: 0, .. })
```

For a non-existing key:

```rs
let bem =  hm.entry(String::from("key1"));
println!("{:?}", bem);

// Entry(VacantEntry("key1"))
```

`or_insert` uses the return value of `entry` to only add the key/value to the
HashMap if the key does not exist and returns a mutable reference to the value
(old value for existing keys and the new value for new keys). Hence, we cannot
use two return values from `or_insert` in the same scope because we will have
two mutable references to (although different) values in the hashmap.

```rs
fn main() {
    use std::collections::HashMap;

    let mut hm = HashMap::new();
    hm.insert(String::from("key0"), 0);

    let key0 = hm.entry(String::from("key0")).or_insert(-1);
    let key1 = hm.entry(String::from("key1")).or_insert(1); // error!

    println!("{:?}", key0);
    println!("{:?}", key1);
}
```

We will get this error:

```
error[E0499]: cannot borrow `hm` as mutable more than once at a time
  --> src/main.rs:8:16
   |
7  |     let key0 = hm.entry(String::from("key0")).or_insert(-1);
   |                ------------------------------ first mutable borrow occurs here
8  |     let key1 = hm.entry(String::from("key1")).or_insert(1);
   |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ second mutable borrow occurs here
9  | 
10 |     println!("{:?}", key0);
   |                      ---- first borrow later used here
```

If we get a reference from `or_insert` we need to dereference to use it.

```rs
fn main() {
    use std::collections::HashMap;

    let mut hm = HashMap::new();
    hm.insert(String::from("key0"), 0);

    let key0 = hm.entry(String::from("key0")).or_insert(-1);
    println!("{:?}", key0);     // 0

    *key0 += 1;
    println!("{:?}", key0);     // 1
}
```

# Chapter 9

## panic!
Ends the program and unwinds the stack (walks back and cleans up). This is
expensive. To prevent clean up and just abort after panic (which is quick), add
this to `Cargo.toml`:

```toml
[profile.release]
panic = 'abort'
```

Use the `panic!` macro:

```rs
fn main() {
    panic!("pewpew");
}

// thread 'main' panicked at 'pewpew', src/main.rs:2:5
// note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

## Recoverable Errors
The `Result` enum can be used to return values from functions that might return
errors.

```rs
enum Result<T, E> {
    Ok(T),      // T: type of value returned in the success case
    Err(E),     // E: type of value returned in case of errors
}
```

Looking at `std::fs::File::open` and we can see:

* Success: `Result<File>`
    * https://doc.rust-lang.org/stable/std/fs/struct.File.html#method.open
* Error: `Err<std::io::Error>`
    * https://doc.rust-lang.org/stable/std/fs/struct.OpenOptions.html#method.open

```rs
use std::fs::File;

fn main() {
    let f = File::open("hello.txt");

    let f = match f {
        Ok(file) => file,
        Err(error) => panic!("Problem opening the file: {:?}", error),
    };
}
```

The code will attempt to open a file. With success, a handle to the file is
stored in `f` and `panic!` otherwise.

## Matching on Different Errors
To act differently based on the error, we can `match` for `error.kind()` in the
error arm.

We are checking if the kind of error is `ErrorKind::NotFound` and if so, we will
create the file. We are also checking if the result of that also returns an
error. For other errors we will just panic.

```rs
use std::fs::File;
use std::io::ErrorKind;

fn main() {
    let f = File::open("hello.txt");

    let f = match f {
        Ok(file) => file,   // file exists
        Err(error) => match error.kind() {  // check the error
            // if file doesn't exist, create it
            ErrorKind::NotFound => match File::create("hello.txt") {
                Ok(fc) => fc,   // new file was created successfully
                Err(e) => panic!("Problem creating the file: {:?}", e), // creating a new file failed
            },
            // all other errors
            other_error => {
                panic!("Problem opening the file: {:?}", other_error)
            }
        },
    };
}
```

There are better ways of writing this code. We will see them in chapter 13.

## unwrap and expect
The `unwrap` method in this code will return the value if there's no error and
calls `panic` otherwise.

```rs
use std::fs::File;

fn main() {
    let f = File::open("hello.txt").unwrap();
}

// thread 'main' panicked at 'called `Result::unwrap()` on an `Err` value: Os {
// code: 2, kind: NotFound, message: "No such file or directory" }',
// src/main.rs:4:37
```

`except` is the same, but we can choose an error message to return along the
default one.

```rs
use std::fs::File;

fn main() {
    let f = File::open("hello.txt").expect("panic!!!");
}

// thread 'main' panicked at 'panic!!!: Os { code: 2, kind: NotFound, message: "No
// such file or directory" }', src/main.rs:4:37
```

## Propagating Errors
We can return errors from our functions. Here's a convoluted way of writing
`FromStr`.


```rs
use std::fs::File;

fn main() {
    match string_to_boolean(String::from("true")) { // "it's true"
        Ok(val) => println!("it's {}", val),
        Err(s) => println!("{}", s),
    }

    match string_to_boolean(String::from("FALse")) { // "it's false"
        Ok(val) => println!("it's {}", val),
        Err(s) => println!("{}", s),
    }

    match string_to_boolean(String::from("trueee")) { // "not boolean"
        Ok(val) => println!("it's {}", val),
        Err(s) => println!("{}", s),
    }
}

fn string_to_boolean(s: String) -> Result<bool, String> {
    // converts a string to boolean. true and false are converted
    // (case-insensitive), everything else is an error

    match s.to_ascii_lowercase().as_ref() {
        "true" => Ok(true),
        "false" => Ok(false),
        _ => Err(String::from("not boolean")),
    }
}
```

## Shortcut for Propagating Errors
Place a `?` after a `Result` value to pass it on. If it's `Ok` then the program
will continue. For `Err` the function will return it.

```rs
use std::fs::File;
use std::io;
use std::io::Read;

fn read_username_from_file() -> Result<String, io::Error> {
    let mut s = String::new();

    File::open("hello.txt")?.read_to_string(&mut s)?;

    Ok(s)
}
```

We will return errors if either of `open` and `.read_to_string` methods
encounter an error. The return value of the function with `?` must match
the parent function.

We can only use the `?` operator in a function that returns `Result` or `Option`
(more but I skipped it for these notes). If the parent function returns
`Option<T>` we can use `?` on a function inside with the same return value.

----------

# Misc
I stopped reading the book. These are my notes from creating projects.

## Type Alias
Type aliases can point to a different type or we can create a new one on the
fly. I mostly used it to create an alias for a type in an external crate.

```rust
type MyType = external_crate::SomeType;

type Point = (u8, u8);
```

https://doc.rust-lang.org/reference/items/type-aliases.html

## Extension Trait
You have an external type, you want to extend it. You can add traits to it.
Think of traits as interfaces.

First, we need to define the trait. By convention, these traits end in `Ext`.

```rust
extern crate crr;
use crr::OtherType;

trait OtherTypeExt {
    fn to_text(&self) -> String;
}
```

Next, implement it.

```rust
impl OtherTypeExt for OtherType {
    fn to_text(&self) -> String {
        // do something.
    }
}
```

Now, we can use it "like a method."

```rust
// in main.rs
let other = OtherType::new();
let text = other.to_text();
```


