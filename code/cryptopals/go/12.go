/*
Byte-at-a-time ECB decryption (Simple)
Copy your oracle function to a new function that encrypts buffers under ECB
mode using a consistent but unknown key (for instance, assign a single random
key, once, to a global variable).

Now take that same function and have it append to the plaintext,
BEFORE ENCRYPTING, the following string:

Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK

Spoiler alert.

Do not decode this string now. Don't do it.

Base64 decode the string before appending it. Do not base64 decode the string
by hand; make your code do it. The point is that you don't know its contents.

What you have now is a function that produces:

AES-128-ECB(your-string || unknown-string, random-key)

It turns out: you can decrypt "unknown-string" with repeated calls to the
oracle function!

Here's roughly how:

1. Feed identical bytes of your-string to the function 1 at a time --- start
with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block size of
the cipher. You know it, but do this step anyway.Detect that the function is
using ECB. You already know, but do this step anyways.

2. Knowing the block size, craft an input block that is exactly 1 byte short
(for instance, if the block size is 8 bytes, make "AAAAAAA").
Think about what the oracle function is going to put in that last byte position.

3. Make a dictionary of every possible last byte by feeding different strings
to the oracle; for instance, "AAAAAAAA", "AAAAAAAB", "AAAAAAAC", remembering
the first block of each invocation.

4. Match the output of the one-byte-short input to one of the entries in your
dictionary. You've now discovered the first byte of unknown-string.

5. Repeat for the next byte.
*/

package main

import (
    "fmt"
    "genericpals"
    "bytes"
)

const (
    MaxBlockSize = 20
)

func main() {
    
    // Detect blocksize
    // Increase input until output length changes, the difference is blocksize

    var blockSize int
    var inp1 []byte

    enc1, err := genericpals.ECBOracle12(inp1)
    if err != nil {
        panic(err)
    }

    originalLength := len(enc1)

    for i:=0; i<MaxBlockSize; i++ {
        inp1 = genericpals.ByteRepeat(byte(0x41), i)
        enc2, err := genericpals.ECBOracle12(inp1)
        if err != nil {
            panic(err)
        }
        
        // If length has changed, we have found blocksize
        if len(enc2) != originalLength {
            blockSize = len(enc2) - originalLength
            break
        }
    }

    fmt.Printf("Blocksize detected: %d\n", blockSize)

    // Detect ECB mode
    // Send in three identical blocks of input and use IsECB
    ecbInput := genericpals.ByteRepeat(byte(0x41), 3*blockSize)
    ecbEnc, err := genericpals.ECBOracle12(ecbInput)
    if err != nil {
        panic(err)
    }
    
    if ecb, _ := genericpals.IsECB(ecbEnc); !ecb {
        fmt.Printf("ECB mode not detected - returning!")
        return
    }

    fmt.Println("ECB Mode: true")

    maxBlocks := originalLength / blockSize

    // Let's just do it for one byte

    // Grab the first block of encrypted text for all iterations of "A"*15 + byte

    var secret []byte

    // For all blocks
    for currentBlock:=0; currentBlock<maxBlocks; currentBlock++ {

        // Do this for each block
        for i:=0; i<blockSize; i++ {

            // fmt.Println("secret")
            // fmt.Println(secret)

            // Create the "AAAAA" that will be sent
            static := genericpals.ByteRepeat(0x41, blockSize-i-1)

            // fmt.Println("static")
            // fmt.Println(static)

            // Grab the result from the oracle
            target, _ := genericpals.ECBOracle12(static)

            // Start bruteforcing
            for j:=0; j<0x100; j++ {
                b := byte(j)

                // Add current known plaintext to start of bruteforce payload
                dynamic := append(static, secret...)

                // Append bruteforce byte
                dynamic = append(dynamic, b)

                // Ask the oracle
                bruteforce, _ := genericpals.ECBOracle12(dynamic)

                // Compare if they match
                cmp1 := bruteforce[currentBlock*16:(currentBlock+1)*16]
                cmp2 := target[currentBlock*16:(currentBlock+1)*16]

                if bytes.Equal(cmp1, cmp2) {

                    // fmt.Println(b)
                    // fmt.Println(i)

                    // Add recovered byte to known bytes
                    secret = append(secret, b)
                    break
                }
            }

        }

    }

    // Unpad PKCS7 - this can be seen after all of unknown bytes is discovered
    secret, _ = genericpals.UnpadPKCS7(secret)

    // Print recovered plaintext
    fmt.Println(string(secret))

}