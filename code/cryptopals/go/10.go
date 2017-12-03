/*
Implement CBC mode
CBC mode is a block cipher mode that allows us to encrypt irregularly-sized
messages, despite the fact that a block cipher natively only transforms
individual blocks.

In CBC mode, each ciphertext block is added to the next plaintext block before
the next call to the cipher core.

The first plaintext block, which has no associated previous ciphertext block,
is added to a "fake 0th ciphertext block" called the initialization vector,
or IV.

Implement CBC mode by hand by taking the ECB function you wrote earlier,
making it encrypt instead of decrypt (verify this by decrypting whatever you
encrypt to test), and using your XOR function from the previous exercise to
combine them.

The file here is intelligible (somewhat) when CBC decrypted against
"YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)
*/

package main

import (
	"crypto/aes"
	"fmt"
	"genericpals"
)

const (
	DataFile  = "data\\10.txt"
	StringKey = "YELLOW SUBMARINE"
)

func main() {

	// Create []byte IV and key
	iv := genericpals.ByteRepeat(0x00, aes.BlockSize)
	key := []byte(StringKey)

	// Read encrypted data from file
	base64Cipher, err := genericpals.ReadAllFile(DataFile)
	if err != nil {
		panic(err)
	}

	// Decode from base64
	byteCipher, err := genericpals.B64DecodeStrToByte(base64Cipher)
	if err != nil {
		panic(err)
	}

	// Decrypt AES-CBC
	plaintext, err := genericpals.DecryptCBC(byteCipher, key, iv)
	if err != nil {
		panic(err)
	}

	// PKCS7 unpad
	unpaddedPlaintext, err := genericpals.UnpadPKCS7(plaintext)
	if err != nil {
		panic(err)
	}

	fmt.Println(string(unpaddedPlaintext))
}
