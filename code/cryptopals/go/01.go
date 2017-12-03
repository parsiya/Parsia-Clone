/*
Convert hex to base64
The string:

49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d
Should produce:

SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
*/

package main

import (
	"fmt"
	"genericpals"
)

const Input = "49276d206b696c6c696e6720796f7572" +
	"20627261696e206c696b65206120706f" +
	"69736f6e6f7573206d757368726f6f6d"
const Output = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

func main() {

	inputBytes := genericpals.Unhexlify(Input)

	b64str := genericpals.B64EncodeByteToStr(inputBytes)

	if b64str == Output {
		fmt.Println("Passed!")
		fmt.Printf("Result: %s", b64str)
		return
	} else {
		fmt.Println("Failed!")
		fmt.Printf("Wanted: %s\nGot: %s", Output, b64str)
	}
}
