---
draft: false
toc: true
comments: false
categories:
- Development
title: "Kotlin Development"
wip: false
snippet: "Notes on Kotlin development, especially Burp extensions."
---

# Kotlin Language Server not Recognizing Burp API
The [Kotlin extension by fwcd][kotlin-ext] language server doesn't recognize
imported libraries in gradle projects.

[kotlin-ext]: https://marketplace.visualstudio.com/items?itemName=fwcd.kotlin

## Build Custom Language Server
Per [BuZZ-dEE's instructions][buzz], I tried building and replacing the language
server:

[buzz]: https://github.com/fwcd/vscode-kotlin/issues/85#issuecomment-2095793958

```bash
# install openjdk 11, you probably need 21 for Burp, too.
sudo apt install msopenjdk-11
git clone https://github.com/fwcd/kotlin-language-server
cd kotlin-language-server
./gradlew :server:installDist
mv ~/.vscode-server/data/User/globalStorage/fwcd.kotlin/langServerInstall/server server-backup
# assuming /kotlin-language-server is where you built the server
cp -r ~/kotlin-language-server/server/build/install/server ~/.vscode-server/data/User/globalStorage/fwcd.kotlin/langServerInstall/
```

Copied the server instead of symlinking per original instructions. Didn't work!

## Troubleshooting Path Issues
Set custom language server path in extension settings:

```json
"kotlin.languageServer.path":
    "~/.vscode-server/data/User/globalStorage/fwcd.kotlin/langServerInstall/server/bin/kotlin-language-server"
```

**Error encountered:**
```
[Error - 11:56:46 AM] Kotlin Language Client client:
    couldn't create connection to server.
Launching server command ~/.vscode-server/data/User/globalStorage/fwcd.kotlin/langServerInstall/server/bin/kotlin-language-server failed. Error: spawn ~/.vscode-server/data/User/globalStorage/fwcd.kotlin/langServerInstall/server/bin/kotlin-language-server ENOENT
```

Which is weird, because I can run the language server manually with that command and it says:

```json
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
Content-Length: 127

{"jsonrpc":"2.0","method":"window/logMessage","params":{"type":3,"message":"main      Kotlin Language Server: Version 1.3.14"}}Content-Length: 108

{"jsonrpc":"2.0","method":"window/logMessage","params":{"type":3,"message":"main      Connected to client"}}
```

Not sure which client it is. Replacing `~` with the complete path runs the
server, but the problem still exists.

### Solution: Different Extension
Gave up on fwcd extension. Use [Kotlin/kotlin-lsp][kotlin-lsp] instead -
download and install the VSIX manually. This one actually works with gradle
projects.

[kotlin-lsp]: https://github.com/Kotlin/kotlin-lsp

----------

# Kotlin Result Type Tutorial
Originally AI generated, but heavily edited.

The `Result<T>` type in Kotlin is similar to Rust's `Result<T, E>`. It forces
you to handle both success and failure cases.

## Simple Example Function

```kotlin
fun divide(a: Int, b: Int): Result<Double> {
  return when (b) {
    0 -> Result.failure(ArithmeticException("Division by zero"))
    else -> Result.success(a.toDouble() / b)
  }
}
```

## Kotlin vs Rust

| Kotlin                  | Rust                            | Description                             |
| ----------------------- | ------------------------------- | --------------------------------------- |
| `getOrElse { default }` | `unwrap_or_else(\|e\| default)` | Get value or compute default from error |
| `getOrNull()`           | `ok()`                          | Get `Some(value)` or `None`             |
| `getOrThrow()`          | `unwrap()`                      | Get value or panic                      |
| `isSuccess`             | `is_ok()`                       | Check if success                        |
| `isFailure`             | `is_err()`                      | Check if error                          |
| `onFailure { }`         | `map_err(\|e\| { })`            | Handle error case                       |
| `onSuccess { }`         | `map(\|v\| { })`                | Handle success case                     |

## 1. `getOrElse` - Provide Default Value

```kotlin
// Simple default value - returns the success value, or 0.0 for failure.
val result = divide(10, 2).getOrElse { 0.0 }
println(result) // 5.0
```

```kotlin
// Handle error and provide fallback - the lambda receives the exception for
// custom handling
val safeResult = divide(10, 0).getOrElse { exception ->
  println("Error: ${exception.message}")
  Double.NaN // Return NaN for division by zero
}
```

## 2. `getOrNull` - Nullable Result

```kotlin
// Returns the success value or null if it failed - enables null-safety patterns
val result = divide(10, 2).getOrNull()
if (result != null) {
    println("Success: $result")
} else {
    println("Operation failed")
}

// With elvis operator - provides default value when result is null
val safeResult = divide(10, 0).getOrNull() ?: 0.0
```

## 3. `getOrThrow` - Throw on Error

```kotlin
// Unwraps success value or throws the original exception - use with try/catch
try {
    val result = divide(10, 2).getOrThrow()
    println("Result: $result")
} catch (e: Exception) {
    println("Caught exception: ${e.message}")
}
```

### 3.1. Exception Propagation Patterns

```kotlin
// Direct propagation - throws the original exception
val result = divide(10, 0).getOrThrow()

// Propagate via getOrElse lambda
val safeResult = divide(10, 0).getOrElse { exception ->
    println("Logging error before re-throwing")
    throw exception
}

// Most idiomatic - return Result and let caller decide
fun processData(): Result<Double> {
  return divide(10, 0)
    .map { it * 2 }     // Transform if successful
    .mapCatching { value ->
      if (value < 0) throw IllegalStateException("Negative result")
      value
    }
}

// Caller handles the final Result
val finalResult = processData().getOrThrow() // or .getOrElse { ... }
```

## 4. Pattern Matching with `when`

```kotlin
// Pattern match on Result type to handle success and failure cases differently
when (val result = divide(10, 0)) {
  is Result.Success -> {
    println("Success: ${result.getOrNull()}")
  }
  is Result.Failure -> {
    val exception = result.exceptionOrNull()
    println("Failed: ${exception?.message}")
  }
}
```

## 5. `onSuccess` and `onFailure` - Side Effects

```kotlin
// Execute side effects (logging, etc.) without consuming the Result - chainable
divide(10, 2)
  .onSuccess { value -> 
    println("Division successful: $value")
  }
  .onFailure { exception ->
    println("Division failed: ${exception.message}")
  }
```

### Using `it` vs Named Parameters
```kotlin
// Using Kotlin's default 'it' parameter - more concise
divide(10, 2)
  .onSuccess { println("Division successful: $it") }  // 'it' = success value
  .onFailure { println("Error: ${it.message}") }      // 'it' = exception

// Using explicit parameter names - more readable for complex lambdas
divide(10, 2)
  .onSuccess { value -> println("Division successful: $value") }
  .onFailure { exception -> println("Error: ${exception.message}") }
```

```kotlin
// Chaining side effects with other operations - the Result flows through unchanged
val finalResult = divide(10, 2)
  .onSuccess { println("Step 1: Division = $it") }
  .map { it * 3 }
  .onSuccess { println("Step 2: Multiplication = $it") }
  .mapCatching { value ->
    if (value > 10) value else throw IllegalArgumentException("Value too small")
  }
  .onSuccess { println("Step 3: Validation passed = $it") }
  .onFailure { println("Error occurred: ${it.message}") }
  .getOrElse { 0.0 }
```

### Checking Status with `isSuccess` and `isFailure`
```kotlin
// Check Result status without consuming the value - useful for conditional logic
val result = divide(10, 0)

if (result.isSuccess) {
  println("Operation succeeded")
} else if (result.isFailure) {
  println("Operation failed")
}
```

## 6. Chaining Operations with `map` and `mapCatching`

```kotlin
val result = divide(20, 4)
  .map { it * 2 }  // Transform success value
  .map { it.toInt() }  // Chain transformations
  .getOrElse { -1 }

println(result) // 10

// mapCatching for operations that might throw
val chainedResult = divide(10, 2)
  .mapCatching { value ->
    if (value > 3) value else throw IllegalArgumentException("Too small")
  }
  .getOrElse { 0.0 }
```

### Best Practices

1. **Use `getOrElse`** for providing sensible defaults.
2. **Use `onFailure`** for logging or side effects without changing the flow.
3. **Use pattern matching** when you need different logic for success/failure.
4. **Use `getOrNull`** when you want to handle null values with standard null-safety.
5. **Avoid `getOrThrow`** unless you're sure the operation should crash on failure.

### Real-World Database Example

```kotlin
fun getUserById(id: Int): Result<User> {
  return Database.query("SELECT * FROM users WHERE id = ?", id)
    .mapCatching { rows ->
      rows.firstOrNull() ?: throw NoSuchElementException("User not found")
    }
    .mapCatching { row ->
      User(
        id = row["id"] as Int,
        name = row["name"] as String,
        email = row["email"] as String
      )
    }
}

// Usage
val user = getUserById(123)
  .onFailure { Log.toError("Failed to get user: ${it.message}") }
  .getOrElse { User.ANONYMOUS }
```