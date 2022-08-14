---
draft: false
toc: true
comments: false
categories:
- Research
title: "Static Program Analysis Notes"
wip: true
snippet: "Notes for the [Static Program Analysis Book](https://cs.au.dk/~amoeller/spa/)"

---

Reading the version dated `February 10, 2022`.

https://cs.au.dk/~amoeller/spa/

I am gonna copy/paste stuff from the PDF and then add my notes instead of
writing digitally on the PDF because I think it will be better for
distribution and searching.

Text from the book is in quotes. I am going to modify some of the quotes to make
them smaller. This is not a critique of the text. I am just making it easier for
ME to understand.

# Preface

> Static program analysis is the art of reasoning about the behavior of computer
> programs without actually running them.

> automated reasoning of software generally must involve approximation

The `Halting Problem` strikes again.

> ensure high precision and efficiency to be practically useful.

> nobody will use [our tool] ... if it reports many false positives or if it is
> too slow to fit into real-world software development processes

There's a case to be made for "slow" scans. We can run them out-of-band. Things
like weekly (or nightly) or per-version scans are also useful.

# Chapter 1: Introduction
Uses of static analysis. I don't need to be convinced that static analysis is
needed.

Rice’s theorem: all interesting questions about the input/output behavior of
programs (written in Turing-complete programming languages) are undecidable.

> [it's] possible to build analysis tools that give useful answers for most
> realistic programs.

**Exercise 1.1**

The code (removed the argc check) so we can just paste it in a REPL.

```c
#include <stdio.h>
#include <string.h>

int main() {
  char *p,*q;
  p = NULL;
  printf("%s",p);   // Just prints (null) in modern compilers, not a security issue

  q = (char *)malloc(100);
  p = q;
  free(q);
  *p = 'x'; // Use-after-free but it's not an error by itself in this code
  printf("%s",p); // Adding this line will trigger the UAF

  free(p);  // Double free

  p = (char *)malloc(100);
  p = (char *)malloc(100); // memory leak because we did not free(p) before the new malloc
  q = p;    // another memory leak? because we did not free(q) before reassigning it
  strcat(p,q);  // Buffer overflow - strcat doesn't do any bounds check
}
```

**End of Exercise 1.1**

> a program analyzer is sound if it never gives incorrect results (but it may
> answer maybe).

Does this mean we can call every static analysis tool `sound`? They could give
us false positives but also say "Well, that was a maybe."

> the notion of soundness depends on the intended application of the analysis
> output

So it depends on the app and its context.

> a verification tool is typically called sound if it never misses any errors of
> the kinds it has been designed to detect, but it is allowed to produce
> spurious warnings (also called false positives),

OK. Then a static analysis tool is `sound` IF it has 100% recall (reports every
issue) with some false positives.

> an automated testing tool is called sound if all reported errors are genuine,
> but it may miss errors.

A sound automated testing tool must have 100% precision (no false positives).

> some static analysis problems are undecidable

**skipped 1.3**

# Chapter 2: A Tiny Imperative Programming Language
Mostly explains the example language's grammar.

**Exercise 2.2:**
Exercise 2.3: Show how the following statement can be normalized:
`x = (**f)(g()+h())`

```
t1 = *f;
t2 = *t1;
t3 = g();
t4 = h();
t5 = t3 + t4;
x = t2(t3);
```

**End of Exercise 2.2:**

## 2.5 Control Flow Graphs

> A control flow graph (CFG) is a directed graph, in which nodes correspond to
> statements and edges represent possible flow of control.

> has a single point of entry and single point of exit

> pred(v): set of predecessor nodes
> succ(v): set of successor nodes

> For programs that are fully normalized each node corresponds to only one
> operation.

# Chapter 3: Type Analysis
Certain operations should only work on certain types. E.g., `*` can only be
called for pointers and `null`.

We cannot guarantee that no types error appear in runtime. So we use an
approximation:

> typability. A program is typable if it satisfies a collection of type
> constraints that is systematically derived, typically from the program AST

In other words we will check for types and as a result any program which passes
our checks will not violate the type requirements.

> the above requirements are guaranteed to hold during execution, but the
> converse is not true. Thus, our type analysis will be conservative and reject
> some programs that in fact will not violate any requirements during execution.

This will reject some programs that might not adhere to these type requirements
but also do not result in runtime errors, but that is OK.

> For a given program we generate a constraint system and define the program to
> be typable when the constraints are solvable.

> A solution assigns a type to each type variable, such that all equality constraints are satisfied.


We create the type constraints for a program and then create a solution that
satisfies the constraint. The solution is basically assigning a type to each
variable. 
 
> The correctness claim for the type analysis is that the existence of a
> solution implies that the specified runtime errors cannot occur during
> execution

But how do we create solutions? Unification

> If solutions exist, then they can be computed in almost linear time using a
> unification algorithm for regular terms

Our type analysis has limitations.

1. It's `flow-insensitive`. For example, it rejects programs where a variable is
   declared as a pointer and is used as an int later while the type changes
   during execution.
2. > Another limitation, which is even more significant from a practical point
   of view, is the current treatment of polymorphic types
3. > it ignores many other kinds of runtime errors, such as dereference of null
   > pointers, reading of uninitialized variables, division by zero, and the
   > more subtle escaping stack cell

# Chapter 4: Lattice Theory
