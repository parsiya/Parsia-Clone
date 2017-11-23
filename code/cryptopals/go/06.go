/*
Break repeating-key XOR
It is officially on, now.

There's a file here. It's been base64'd after being encrypted with repeating-key XOR.

Decrypt it.

Here's how:

1. Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.

2. Write a function to compute the edit distance/Hamming distance between two
strings. The Hamming distance is just the number of differing bits.

The distance between:

this is a test and wokka wokka!!!

is 37. Make sure your code agrees before you proceed.

3. For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second
KEYSIZE worth of bytes, and find the edit distance between them.
Normalize this result by dividing by KEYSIZE.

4.The KEYSIZE with the smallest normalized edit distance is probably the key.
You could proceed perhaps with the smallest 2-3 KEYSIZE values.
Or take 4 KEYSIZE blocks instead of 2 and average the distances.

5. Now that you probably know the KEYSIZE: break the ciphertext into blocks of
KEYSIZE length.

6. Now transpose the blocks: make a block that is the first byte of every block,
and a block that is the second byte of every block, and so on.

7. Solve each block as if it was single-character XOR. You already have code to
do this.

8. For each block, the single-byte XOR key that produces the best looking
histogram is the repeating-key XOR key byte for that block. Put them together
and you have the key.

9. This code is going to turn out to be surprisingly useful later on.
Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic
exercise, a "Crypto 101" thing. But more people "know how" to break it than can
actually break it, and a similar technique breaks something much more important.
*/

package main

import (
    "genericpals"
    "fmt"
    "sort"
)

const (
    HammingTest1 = "this is a test"
    HammingTest2 = "wokka wokka!!!"

    DataFile = "data\\06.txt"

    // # of sequential bytes used in calculating the normalized hamming distance
    // This allows us to finetune the keysize
    // Note, this will result in error if Num*keysize > len(ciphertext)
    Num = 20

    // # of top keysize choices used for bruteforcing
    Top = 5

    // Minimum keysize used in Hamming distance test
    MinKeySize = 2

    // Maximum keysize used in Hamming distance test
    MaxKeySize = 40

)


func main() {

    hammingBytes1 := []byte(HammingTest1)
    hammingBytes2 := []byte(HammingTest2)

    testDist := genericpals.HammingDistance(hammingBytes1, hammingBytes2)

    // Test HammingDistance function
    if testDist != 37 {
        panic("Wrong distance")
        return
    }

    // Read base64 from input file without EOL
    inputString, err := genericpals.ReadAllFile(DataFile)
    if err != nil {
        panic(err)
    }

    // Convert from base64 to decoded []byte
    cipherBytes, err := genericpals.B64DecodeStrToByte(inputString)
    if err != nil {
        panic(err)
    }
    
    type ham struct {
        Keysize int
        AvgDist float32
    }

    var hammings []ham

    // For key sizes 2 to 40
    for keysize:=MinKeySize; keysize<MaxKeySize; keysize++ {

        var hammingTotal float32

        for n:=0; n<Num; n++ {
            block1, block2 := genericpals.GetTwoSeqBytes(cipherBytes, keysize, n)

            hammingTotal += float32(genericpals.HammingDistance(block1, block2))
        }

        avgHamming := hammingTotal / float32(Num*keysize)

        hammings = append(hammings, ham{Keysize: keysize, AvgDist: avgHamming})
    }

    // Sort by distance (ascending)
    sort.Slice(hammings, func(i, j int) bool {
        return hammings[i].AvgDist < hammings[j].AvgDist
    })

    // Get Top keys
    topKeySizes := hammings[:Top]

    // Struct to hold the results
    type breakXORResults struct {
        Key []byte
        PrintableScore float64
        Plaintext string
    }

    topResults := make([]breakXORResults, Top)

    for index, key := range topKeySizes {
        blobs := make([][]byte, key.Keysize)

        // Divide bytes into slices
        for j := 0; j < len(cipherBytes); j++ {
            blobs[j % key.Keysize] = append(blobs[j % key.Keysize], cipherBytes[j])
        }

        secretKey := make([]byte, key.Keysize)

        // Break each one
        for k := 0; k < key.Keysize; k++ {
            tempResult := genericpals.BreakSingleByteXOR(blobs[k])

            secretKey[k] = tempResult.Key
        }
        
        plaintext := genericpals.XOR(cipherBytes, secretKey)
        topResults[index].Plaintext = string(plaintext)
        topResults[index].Key = secretKey
        topResults[index].PrintableScore = genericpals.PrintableEnglish(plaintext)

        // fmt.Printf("Keysize: %v - Key: %v\n", key, string(secretKey))
    }

    // Now we have all the good stuff

    // Sort top results by PrintableScore descending
    sort.Slice(topResults, func(i, j int) bool {
        return topResults[i].PrintableScore > topResults[j].PrintableScore
    })

    // Print the best we have
    fmt.Printf("Key: %v\n", string(topResults[0].Key))
    fmt.Printf("Plaintext\n\n%v", topResults[0].Plaintext)
}