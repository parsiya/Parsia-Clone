/*
PKCS#7 padding validation
Write a function that takes a plaintext, determines if it has valid PKCS#7
padding, and strips the padding off.

The string:

"ICE ICE BABY\x04\x04\x04\x04"
... has valid padding, and produces the result "ICE ICE BABY".

The string:

"ICE ICE BABY\x05\x05\x05\x05"
... does not have valid padding, nor does:

"ICE ICE BABY\x01\x02\x03\x04"
If you are writing in a language with exceptions, like Python or Ruby,
make your function throw an exception on bad padding.

Crypto nerds know where we're going with this. Bear with us.
*/

// I already this with UnpadPKCS7

package main

import (
	"fmt"
	"genericpals"
)

func main() {

	validPadding := append([]byte("ICE ICE BABY"),
		genericpals.ByteRepeat(0x04, 4)...)

	invalidPadding1 := append([]byte("ICE ICE BABY"),
		genericpals.ByteRepeat(0x05, 4)...)

	invalidPadding2 := append([]byte("ICE ICE BABY"),
		genericpals.Unhexlify("01020304")...)

	unpad1, err := genericpals.UnpadPKCS7(validPadding)
	if err != nil {
		fmt.Println("Invalid padding")
	}
	fmt.Println(string(unpad1))

	unpad2, err := genericpals.UnpadPKCS7(invalidPadding1)
	if err != nil {
		fmt.Println("Invalid padding")
	}
	fmt.Println(unpad2)

	unpad3, err := genericpals.UnpadPKCS7(invalidPadding2)
	if err != nil {
		fmt.Println("Invalid padding")
	}
	fmt.Println(unpad3)

}
