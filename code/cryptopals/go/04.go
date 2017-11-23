/*
Detect single-character XOR
One of the 60-character strings in this file has been encrypted by single-character XOR.

Find it.

(Your code from #3 should help.)
*/

package main

import (
    "genericpals"
    "fmt"

)

const FileName = "data\\04.txt"

func main() {

    ciphers, _ := genericpals.ReadLines(FileName)

    var bestResult genericpals.Result

    for i := 0; i < len(ciphers); i++ {

        byteCipher := genericpals.Unhexlify(ciphers[i])

        tempResult := genericpals.BreakSingleByteXOR(byteCipher)

        if tempResult.PrintableScore > bestResult.PrintableScore {
            bestResult = tempResult
        }
    }

    fmt.Printf("%#v\n", bestResult)
}