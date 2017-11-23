/*
Implement PKCS#7 padding
A block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of
plaintext into ciphertext. But we almost never want to transform a single block;
we encrypt irregularly-sized messages.

One way we account for irregularly-sized messages is by padding, creating a
plaintext that is an even multiple of the blocksize. The most popular padding
scheme is called PKCS#7.

So: pad any block to a specific block length, by appending the number of bytes
of padding to the end of the block. For instance,

"YELLOW SUBMARINE"
... padded to 20 bytes would be:

"YELLOW SUBMARINE\x04\x04\x04\x04"
*/

package main

import (
    "genericpals"
    "fmt"
)

func main() {
    
    unpadded  := "YELLOW SUBMARINE"
    blockSize := 20

    padded := genericpals.PKCS7Pad([]byte(unpadded), blockSize)

    fmt.Println(padded)
    fmt.Println(string(padded))

    // Check if we add a full block of padding if input is a multiple of
    // block size. This is done to prevent data lose.
    // For example if the last byte of input is 0x01, how do we know if it's
    // padding or real data. This way we know it's real data because we have
    // one full block of padding after that.
    // As a result when unpadding, we know there's always padding to remove.
    fmt.Println((genericpals.PKCS7Pad([]byte("0123456789"), 10)))
    fmt.Println((genericpals.PKCS7Pad([]byte("Hello"), 5)))

}