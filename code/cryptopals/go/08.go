/*
Detect AES in ECB mode
In this file are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic;
the same 16 byte plaintext block will always produce the same 16 byte ciphertext.
*/

package main

import (
    "genericpals"
    "bytes"
    "fmt"
    "crypto/aes"
)

const DataFile = "data\\08.txt"


func main() {
    allCiphers, err := genericpals.ReadLines(DataFile)

    if err != nil {
        panic(err)
    }

    for _, cipher := range allCiphers {

        // Convert to byte
        byteCipher := genericpals.Unhexlify(cipher)

        // Split into 16 byte
        splits := genericpals.SplitBytes(byteCipher, aes.BlockSize)

        count := 0

        for _, part := range splits {

            count += (bytes.Count(byteCipher, part) - 1)
        }

        if count > 1 {
            for _, part := range splits {
                fmt.Println(genericpals.Hexlify(part))
            }
        }
    }
}