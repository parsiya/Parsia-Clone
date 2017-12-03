/*
Single-byte XOR cipher
The hex encoded string:

1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character.
Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext.
Character frequency is a good metric.
Evaluate each output and choose the one with the best score.
*/

package main

import (
	"fmt"
	"genericpals"
)

const CipherText = "1b37373331363f78151b7f2b783431333" +
	"d78397828372d363c78373e783a393b3736"

func main() {
	ciphertext := genericpals.Unhexlify(CipherText)

	result := genericpals.BreakSingleByteXOR(ciphertext)

	fmt.Printf("Key: 0x%x\nPlaintext: %s", result.Key, result.Plaintext)

}
