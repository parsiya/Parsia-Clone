/*
ECB cut-and-paste
Write a k=v parsing routine, as if for a structured cookie. The routine should
take:

foo=bar&baz=qux&zap=zazzle

and produce:

{
  foo: 'bar',
  baz: 'qux',
  zap: 'zazzle'
}

(you know, the object; I don't care if you convert it to JSON).

Now write a function that encodes a user profile in that format, given an
email address. You should have something like:

profile_for("foo@bar.com")

and it should produce:

{
  email: 'foo@bar.com',
  uid: 10,
  role: 'user'
}

encoded as:

email=foo@bar.com&uid=10&role=user

Your "profile_for" function should not allow encoding metacharacters (& and =).
Eat them, quote them, whatever you want to do, but don't let people set their
email address to "foo@bar.com&role=admin".

Now, two more easy functions. Generate a random AES key, then:

A. Encrypt the encoded user profile under the key; "provide" that to the "attacker".

B. Decrypt the encoded user profile and parse it.

Using only the user input to profile_for()
(as an oracle to generate "valid" ciphertexts) and the ciphertexts themselves,
make a role=admin profile.
*/

package main

import (
	"fmt"
	"genericpals"
	"strings"
)

const (
	MaxBlockSize = 20
)

func main() {

	// JSON tests
	// query := "foo=bar&baz=qux&zap=zazzle"
	// js, _ := genericpals.QueryToJSON(query)
	// fmt.Println(string(js))
	// nem, _ := json.Unmarshal(jsonString)
	// fmt.Println(string(nem))

	// Profile encrypt-decrypt-tests
	// fmt.Println(genericpals.ProfileFor13("nem@nem.com"))

	// nem, err := genericpals.EncryptProfile13("nem@nem.com")
	// if err != nil {
	//     panic(err)
	// }

	// fmt.Println(genericpals.Hexlify(nem))

	// dec, err := genericpals.DecryptProfile13(nem)
	// if err != nil {
	//     panic(err)
	// }

	// fmt.Println(dec)

	// Detect blocksize - from challenge 12
	// Increase input until output length changes, the difference is blocksize

	var blockSize int
	var inp1 string

	enc1, err := genericpals.EncryptProfile13(inp1)
	if err != nil {
		panic(err)
	}

	originalLength := len(enc1)

	for i := 0; i < MaxBlockSize; i++ {
		inp1 = strings.Repeat("A", i)
		enc2, err := genericpals.EncryptProfile13(inp1)
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

	// So here's how it works - we are taking advantage of whitespace too
	// First we send this payload (without quotes):
	// "12@345.comadmin           " - 11 spaces to send admin to next block
	// This will be encoded as:
	// email=12@345.com
	// admin+++++++++++  <-- we want this block (+ = space)
	// &uid=10&role=user
	// Now we have the ciphertext block that just says admin and a bunch of +
	//
	// Then we send another payload:
	// "12@345.com   " - 3 spaces to send user to next block
	// We get ciphertext for
	// email=12%403.com  <-- we want this block
	// +++&uid=10&role=  <-- we want this block too
	// user
	//
	// Now we have the ciphertext block that says
	// "email=12%403.com+++&uid=10&role="
	// Append the ciphertext block for "admin+++++++++++"
	// Spaces have been converted to + but they will be ignored when parsing

	inp3 := "12@345.comadmin           "
	enc3, _ := genericpals.EncryptProfile13(inp3)
	dec3, _ := genericpals.DecryptProfile13(enc3)

	// Grabbing second block for admin
	adminBlock := enc3[16:32]

	fmt.Println(dec3)

	inp4 := "12@345.com   "
	enc4, _ := genericpals.EncryptProfile13(inp4)
	dec4, _ := genericpals.DecryptProfile13(enc4)

	// Grabbing first and second block
	userBlock := enc4[0:32]

	fmt.Println(dec4)

	craftedProfile := append(userBlock, adminBlock...)

	dec5, err := genericpals.DecryptProfile13(craftedProfile)
	if err != nil {
		panic(err)
	}

	fmt.Println(dec5)

}
