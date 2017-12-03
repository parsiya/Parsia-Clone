/*
Byte-at-a-time ECB decryption (Harder)
Take your oracle function from #12. Now generate a random count of random bytes
and prepend this string to every plaintext. You are now doing:

AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)

Same goal: decrypt the target-bytes.

Stop and think for a second.

What's harder than challenge #12 about doing this? How would you overcome that
obstacle? The hint is: you're using all the tools you already have; no crazy
math is required.

Think "STIMULUS" and "RESPONSE".
*/

// So I had this all wrong, the length of the prefix is fixed but unknown

package main

import (
	"bytes"
	"fmt"
	"genericpals"
)

const (
	MaxBlockSize = 20
)

func main() {

	// Detect blocksize - from challenge 12
	// Increase input until output length changes, the difference is blocksize

	var blockSize int
	var inp1 []byte

	enc1, err := genericpals.ECBOracle14(inp1)
	if err != nil {
		panic(err)
	}

	originalLength := len(enc1)

	for i := 0; i < MaxBlockSize; i++ {
		inp1 = genericpals.ByteRepeat(0x41, i)
		enc2, err := genericpals.ECBOracle14(inp1)
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

	// Now we need to detect prefix length
	// Start with a zero length payload
	// Increase payload length until we get two equal blocks
	// Which will look like
	// [prefix]|[prefix]AAAA|[block of A]|[block of A]
	// Then prefix % blocksize == 3*blockSize - len(payload)
	// This is exactly what IsECB mode does so we are detecting ECB mode and
	// prefix padding in one go
	var prefixLen int
	for payloadLen := 0; payloadLen < 3*blockSize; payloadLen++ {

		payload := genericpals.ByteRepeat(0x41, payloadLen)
		enc3, err := genericpals.ECBOracle14(payload)
		if err != nil {
			panic(err)
		}

		isECB, err := genericpals.IsECB(enc3)
		if err != nil {
			panic(err)
		}

		if isECB {
			prefixLen = 3*blockSize - payloadLen
			break
		}
	}

	// Notice we cannot detect the exact prefix length but mod blockSize
	// And that's the only thing we need
	fmt.Printf("Prefix length %% %d = %d\n", blockSize, prefixLen)

	// This might not work if prefix is more than one blocks
	maxBlocks := originalLength / blockSize

	// Let's just do it for one byte

	// Grab the first block of encrypted text for all iterations of "A"*15 + byte

	var secret []byte
	var static []byte

	// Fill prefix block to get to the next one
	prefixFill := genericpals.ByteRepeat(0x42, blockSize-prefixLen)

	// For all blocks
	// The starting block needs to be detected based on how many blocks the
	// prefix is. For example our prefix fills one block and a half, we fill the
	// second block with our padding and then start at third block.
	for currentBlock := 2; currentBlock < maxBlocks; currentBlock++ {

		// Do this for each block
		for i := 0; i < blockSize; i++ {
			fmt.Printf("%s\n-------\n", string(secret))

			static = prefixFill
			// Create the "AAAAA" that will be sent
			static = append(static, genericpals.ByteRepeat(0x41, blockSize-i-1)...)

			// fmt.Println("static")
			// fmt.Println(static)

			// Grab the result from the oracle
			target, _ := genericpals.ECBOracle14(static)

			// Start bruteforcing
			for j := 0; j < 0x100; j++ {
				b := byte(j)

				// Add current known plaintext to start of bruteforce payload
				dynamic := append(static, secret...)

				// Append bruteforce byte
				dynamic = append(dynamic, b)

				// Ask the oracle
				bruteforce, _ := genericpals.ECBOracle14(dynamic)

				// Compare if they match
				cmp1 := bruteforce[currentBlock*16 : (currentBlock+1)*16]
				cmp2 := target[currentBlock*16 : (currentBlock+1)*16]

				if bytes.Equal(cmp1, cmp2) {

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
