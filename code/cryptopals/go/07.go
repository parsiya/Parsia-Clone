/*
AES in ECB mode
The Base64-encoded content in this file has been encrypted via
AES-128 in ECB mode under the key

"YELLOW SUBMARINE".
(case-sensitive, without the quotes; exactly 16 characters; I like
"YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).

Decrypt it. You know the key, after all.

Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.
*/

package main

import (
    "genericpals"
    "fmt"
)

const (
    Key = "YELLOW SUBMARINE"
    DataFile = "data\\07.txt"
)

func main() {

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
    
    // Convert Key to []byte
    key := []byte(Key)

    plaintext, err := genericpals.DecryptECB(cipherBytes, key)

    if err != nil {
        panic(err)
    }

    // Last 4 bytes will be padding 0x04
    plaintext, _ = genericpals.UnpadPKCS7(plaintext)

    fmt.Printf("%s", string(plaintext))
}