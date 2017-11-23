/*
Fixed XOR
Write a function that takes two equallength buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:-

1c0111001f010100061a024b53535009181c
... after hex decoding, and when XOR'd against:

686974207468652062756c6c277320657965
... should produce:

746865206b696420646f6e277420706c6179
*/

package main

import (
    "fmt"
    "genericpals"
)

const Input1 = "1c0111001f010100061a024b53535009181c"
const Input2 = "686974207468652062756c6c277320657965"
const Output = "746865206b696420646f6e277420706c6179"

func main() {
    bytes1 := genericpals.Unhexlify(Input1)
    bytes2 := genericpals.Unhexlify(Input2)
    output := genericpals.Unhexlify(Output)

    out, err := genericpals.SameLengthXOR(bytes1, bytes2)
    if err != nil {
        panic(err.Error())
    } else {
        if genericpals.ByteArrayEqual(out, output) {
            fmt.Println("Passed!")
            fmt.Printf("Result: %s", out)
        } else {
            fmt.Println("Failed!")
            fmt.Printf("Wanted: %s\nGot: %s", Output, out)
        }
    }
}