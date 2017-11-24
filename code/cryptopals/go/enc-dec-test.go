// Encryption and decryption tests

package main

import (
    "fmt"
    "genericpals"
)

func main() {
    
    // Create some random plaintext
    plain1 := []byte("ECB-Encrypt-Decrypt-123123123123123123")
    plain1  = genericpals.PadPKCS7(plain1, 16)

    // Create a random key
    key := genericpals.RandomBytes(16)

    encECB, err := genericpals.EncryptECB(plain1, key)
    if err != nil {
        panic(err)
    }
    
    decECB, _ := genericpals.DecryptECB(encECB, key)

    decrypted, _ := genericpals.UnpadPKCS7(decECB)

    fmt.Println(string(decrypted))

    plain2 := []byte("CBC-Encrypt-Decrypt`12`12`2`2`")
    plain2  = genericpals.PadPKCS7(plain2, 16)

    fmt.Println(genericpals.Hexlify(plain2))

    key2 := genericpals.RandomBytes(16)
    iv   := genericpals.RandomBytes(16)

    fmt.Println(genericpals.Hexlify(key2))
    fmt.Println(genericpals.Hexlify(iv))

    encCBC, err := genericpals.EncryptCBC(plain2, key2, iv)
    if err != nil {
        panic(err)
    }

    fmt.Println(genericpals.Hexlify(encCBC))
    
    decCBC, err := genericpals.DecryptCBC(encCBC, key2, iv)
    if err != nil {
        panic(err)
    }
    
    fmt.Println(genericpals.Hexlify(decCBC))

    fmt.Println(string(decCBC))
}