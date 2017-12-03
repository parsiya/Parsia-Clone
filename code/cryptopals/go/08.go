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
	"crypto/aes"
	"fmt"
	"genericpals"
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

		isECB, err := genericpals.IsECB(byteCipher)
		if err != nil {
			panic(err)
		}

		if isECB {
			splits := genericpals.SplitBytes(byteCipher, aes.BlockSize)
			for _, part := range splits {
				fmt.Println(genericpals.Hexlify(part))
			}
		}
	}
}
