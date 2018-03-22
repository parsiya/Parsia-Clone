// Collection of utilities

package genericpals

import (
	"bufio"
	"bytes"
	"crypto/aes"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"math/bits"
	"math/rand"
	"net/url"
	"os"
	"sort"
	"strings"
	"time"
	// "reflect"
)

// Unhexlify converts an ASCII-Hex encoded string to the corresponding []byte
// Params:
//      hexString: string containing bytes
//
// Return: []byte converted from ASCII-Hex
func Unhexlify(hexString string) []byte {
	hexlified, err := hex.DecodeString(hexString)
	if err != nil {
		panic(err)
		return nil
	} else {
		return hexlified
	}
}

// Hexlify converts a []byte to ASCII-Hex
// Params:
//      inputBytes: []byte containing ASCII-Hex bytes
//
// Return: string containing ASCII-Hex representation of []byte
func Hexlify(inputBytes []byte) string {
	return hex.EncodeToString(inputBytes)
}

// B64EncodeByteToStr encode a []byte in base64 standard
// Params:
//      inputBytes: []byte that will be encoded to base64
//
// Return: string containing base64 encoded data
func B64EncodeByteToStr(inputBytes []byte) string {
	return base64.StdEncoding.EncodeToString(inputBytes)
}

// B64DecodeStrToByte decodes a string and returns the result in []byte
// Params:
//      inputString: base64 encoded string
//
// Return: []byte containing decoded bytes
func B64DecodeStrToByte(inputString string) ([]byte, error) {
	decoded, err := base64.StdEncoding.DecodeString(inputString)
	if err != nil {
		return nil, err
	}
	return decoded, nil
}

// SameLengthXOR XORs two []byte of same length
// Params:
//      inputBytes1, inputBytes2: []byte containing strings to be XOR-ed
//
// Return: XOR result and error if applicable
func SameLengthXOR(inputBytes1 []byte, inputBytes2 []byte) ([]byte, error) {
	if len(inputBytes1) != len(inputBytes2) {
		return nil, fmt.Errorf("input1 length %d != %d Input2 length",
			len(inputBytes1), len(inputBytes2))
	} else {
		// Make a slice because Go does not have dynamic-length arrays
		outputBytes := make([]byte, len(inputBytes1))
		for i := 0; i < len(inputBytes1); i++ {
			outputBytes[i] = inputBytes1[i] ^ inputBytes2[i]
		}
		return outputBytes, nil
	}
}

// ByteArrayEqual return true if []bytes are of the same length and have the
// same bytes
// Params:
//      inputBytes1, inputBytes2: []bytes to be compared
//
// Return: true if equal, otherwise false
func ByteArrayEqual(inputBytes1 []byte, inputBytes2 []byte) bool {
	return bytes.Equal(inputBytes1, inputBytes2)
}

// SingleByteXOR XORs a single byte key with a []byte
// Params:
//      key: Single byte key
//      inputBytes: []byte to be XOR-ed
//
// Return: XOR-ed []byte
func SingleByteXOR(inputBytes []byte, key byte) []byte {
	outputBytes := make([]byte, len(inputBytes))
	for i := 0; i < len(inputBytes); i++ {
		outputBytes[i] = inputBytes[i] ^ key
	}
	return outputBytes
}

// isPrintableASCII returns true if input's ASCII-Hex code is
// between 0x20 [inclusive] and 0x7F. See an ASCII table for more info.
// Trust me, I am a pseudo reverse engineer
// Params:
//      char: byte char to be evaluated
//
// Return: true if char is printable, false if not
func isPrintableASCII(char byte) bool {
	return ((0x20 <= char) && (char < 0x7F))
}

// English letter frequency array
// Cannot have const maps in go
var frequency = map[string]float64{
	"a": 0.0651738,
	"b": 0.0124248,
	"c": 0.0217339,
	"d": 0.0349835,
	"e": 0.1041442,
	"f": 0.0197881,
	"g": 0.0158610,
	"h": 0.0492888,
	"i": 0.0558094,
	"j": 0.0009033,
	"k": 0.0050529,
	"l": 0.0331490,
	"m": 0.0202124,
	"n": 0.0564513,
	"o": 0.0596302,
	"p": 0.0137645,
	"q": 0.0008606,
	"r": 0.0497563,
	"s": 0.0515760,
	"t": 0.0729357,
	"u": 0.0225134,
	"v": 0.0082903,
	"w": 0.0171272,
	"x": 0.0013692,
	"y": 0.0145984,
	"z": 0.0007836,
	" ": 0.1918182,
}

// PrintableEnglish returns a score based on closeness of the input string to
// the English language
// All chars are parsed, for each char with a value in the frequency map, the
// score is increased by the frequency value
// Params:
//      textBytes: Input string in []byte
//
// Returns: Score in float32
func PrintableEnglish(textBytes []byte) float64 {

	var score float64
	for _, char := range textBytes {
		ch := strings.ToLower(string(char))
		if frequency[ch] != 0 {
			score += frequency[ch]
		} else {
			score -= 0.01
		}
	}
	return score
}

// Struct to hold the results
type Result struct {
	Key            byte
	PrintableScore float64
	Plaintext      string
}

// BreakSingleByteXOR attempts to break single byte XOR encryption.
// It uses printableEnglish to find the one with the highest score and
// returns the struct
// Params:
//      ciphertext: []byte containing single-byte XOR encrypted string
//
// Return: genericpals.Result
func BreakSingleByteXOR(ciphertext []byte) Result {

	results := make([]Result, 0x100)

	for key := 0; key < 0x100; key++ {
		plaintext := SingleByteXOR(ciphertext, byte(key))

		results[key].Plaintext = string(plaintext)
		results[key].Key = byte(key)
		results[key].PrintableScore = PrintableEnglish(plaintext)

	}

	// Sorting the array using sort.Slice
	// https://stackoverflow.com/a/42872183

	// Sort
	sort.Slice(results[:], func(i, j int) bool {
		return results[i].PrintableScore > results[j].PrintableScore
	})

	return results[0]
}

// ReadLines reads lines from a text file and stores each in an element of a
// string array
// Params:
//      filePath: string containing path to file
//
// Return: []string containing each line in one element and error if applicable.
// How to read lines using go
// https://stackoverflow.com/a/16615559
// "Scanner does not deal well with lines longer than 65536 characters."
func ReadLines(filePath string) ([]string, error) {

	inputFile, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}

	// Close the file after function returns
	defer inputFile.Close()

	var textLines []string

	scanner := bufio.NewScanner(inputFile)

	for scanner.Scan() {
		textLines = append(textLines, scanner.Text())
	}

	return textLines, scanner.Err()
}

// XOR XORs a key with a []byte and repeats the key
// Params:
//      key: []byte key
//      inputBytes: []byte to be XOR-ed
//
// Return: XOR-ed []byte
func XOR(inputBytes []byte, key []byte) []byte {
	outputBytes := make([]byte, len(inputBytes))

	keyLen := len(key)

	for i := 0; i < len(inputBytes); i++ {
		outputBytes[i] = inputBytes[i] ^ key[i%keyLen]
	}

	return outputBytes
}

// HammingDistance calculates the hamming distance between two []byte strings
// XOR two bytes and then count the 1 bits in result
// Params:
//      stringBytes1, stringBytes2: []byte
//
// Return: Hamming distance as int
func HammingDistance(stringBytes1 []byte, stringBytes2 []byte) int {
	if len(stringBytes1) != len(stringBytes2) {
		panic("input bytes are not of same length")
		return -1
	}

	dist := 0

	for i := 0; i < len(stringBytes1); i++ {
		// Thanks Travis
		d1 := bits.OnesCount8(stringBytes1[i] ^ stringBytes2[i])
		dist += d1
	}

	return dist
}

// ReadAllFile is similar to ReadLines but returns one string instead of each
// line being in one string
// Params:
//      filePath: string containing path to file
//
// Return: string containing all characters in the file with new lines removed
func ReadAllFile(filePath string) (string, error) {
	inputFile, err := os.Open(filePath)
	if err != nil {
		return "", err
	}

	// Close the file after function returns
	defer inputFile.Close()

	var allLines string

	scanner := bufio.NewScanner(inputFile)

	for scanner.Scan() {
		allLines += scanner.Text()
	}

	return allLines, scanner.Err()
}

// GetTwoSeqBytes returns n-th two sequential blocks of size bytes from input
// Params:
//      inputBytes: input []byte
//      size      : size of selected bytes
//      n         : n-th tuple (how do I say it in English lol?)
//
// Returns: Two sequential []byte of same size
func GetTwoSeqBytes(input []byte, size int, n int) (block1, block2 []byte) {

	// 0 is unnecessary but this will be readable 6 months down the road
	block1 = input[(2*n+0)*size : (2*n+1)*size]
	block2 = input[(2*n+1)*size : (2*n+2)*size]

	return block1, block2
}

// EncryptECB encrypts []byte plaintext to []byte ciphertext
// Params:
//      plaintext: []byte plaintext
//      key      : []byte key
//
// Return: []byte ciphertext and error if any
func EncryptECB(plaintext []byte, key []byte) ([]byte, error) {

	// 1. Check if plaintext is a multiple of 16
	if len(plaintext)%16 != 0 {
		return nil, fmt.Errorf("plaintext is %d bytes which is not "+
			"a multiple of 16.", len(plaintext))
	}

	// 2. Check if key and 16 are of same length
	if len(key) != 16 {
		return nil, fmt.Errorf("key has wrong length.\nexpected %d, got %d",
			16, len(key))
	}

	// 3. Get an AES block
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	ciphertext := make([]byte, len(plaintext))

	// 4. Encrypt each block individually and store
	for i := 0; i < len(plaintext); i += 16 {
		block.Encrypt(ciphertext[i:i+16], plaintext[i:i+16])
	}

	return ciphertext, nil
}

// DecryptECB decrypt []byte ciphertext to []byte plaintext
// Params:
//      ciphertext: []byte ciphertext
//      key       : []byte key
//
// Return: []byte plaintext and error if any
func DecryptECB(ciphertext []byte, key []byte) ([]byte, error) {

	// 1. Check if ciphertext is a multiple of 16
	if len(ciphertext)%16 != 0 {
		return nil, fmt.Errorf("ciphertext is %d bytes which is not "+
			"a multiple of 16.", len(ciphertext))
	}

	// 2. Check if key and 16 are of same length
	if len(key) != 16 {
		return nil, fmt.Errorf("key has wrong length.\nexpected %d, got %d",
			16, len(key))
	}

	// 3. Get an AES block
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	plaintext := make([]byte, len(ciphertext))

	for i := 0; i < len(ciphertext); i += 16 {
		block.Decrypt(plaintext[i:i+16], ciphertext[i:i+16])
	}

	return plaintext, nil
}

// SplitBytes splits a []byte into equal lengths of n
// Last section may be smaller than the rest.
// Params:
//      inputBytes: []byte
//      n: int - split length
//
// Return: [][]byte
func SplitBytes(inputBytes []byte, n int) [][]byte {

	size := len(inputBytes) / n
	if (len(inputBytes) % n) != 0 {
		size += 1
	}

	splits := make([][]byte, size)

	for i := 0; i < len(inputBytes); i += n {

		if i+n > len(inputBytes) {
			splits[i/n] = inputBytes[i:len(inputBytes)]
		} else {
			splits[i/n] = inputBytes[i : i+n]
		}
	}

	return splits
}

// ByteRepeat creates a []byte by repeating a byte
// It works the same way as bytes.Repeat([]byte, count) but accepts a single byte
// Params:
//      repeatByte: byte to be repeated
//      n: int - number of times to repeat repeatByte
//
// Returns: []byte containing repeatByte n times
func ByteRepeat(repeatByte byte, n int) []byte {

	if n < 0 {
		panic("negative repeat count")
	}

	output := make([]byte, n)

	for i := 0; i < n; i++ {
		output[i] = repeatByte
	}

	return output
}

// IsECB attempts to detect ECB mode based on repeated blocks
// Input is split into 16 and then a score is calculated where it's
// incremented by the number of repeated blocks minus the original
// Params:
//      ciphertext: []byte containing ciphertext
//
// Return: true if ECB mode is detected and error if applicable
func IsECB(ciphertext []byte) (bool, error) {

	if len(ciphertext)%16 != 0 {
		return false, fmt.Errorf("ciphertext is not a multiple of %d", 16)
	}

	// Split into 16 byte
	splits := SplitBytes(ciphertext, 16)

	count := 0

	// Calculate the number of occurrences-1
	for _, block := range splits {
		count += (bytes.Count(ciphertext, block) - 1)
	}

	if count > 1 {
		return true, nil
	}

	return false, nil
}

// PadPKCS7 pads a []byte to a multiple of blockSize
// Padding value is the number of padded bytes
// For example if we are padding 4 bytes, padding value will be 0x04
// Params:
//      bytesToPad: []byte - unpadded input
//      blockSize : int - input will be padded to a multiple of this number
//
// Return: []byte - padded input
// If input is exactly a multiple of blockSize, we add a complete block of
// padding. This is done to differentiate between the last byte of input being
// 0x01 vs. when the last block is 15 bytes and it gets a 0x01 padding byte
func PadPKCS7(bytesToPad []byte, blockSize int) []byte {

	if len(bytesToPad) == 0 {
		panic("cannot pad an empty []byte")
	}

	paddingSize := blockSize - (len(bytesToPad) % blockSize)

	// bytes.Repeat needs []byte - we have int
	// Thus we use our own function
	padding := ByteRepeat(byte(paddingSize), paddingSize)

	// Second param of append needs the primitive time of the first param
	// For example in this case bytesToPad is []byte so padding should be byte
	// But because it's []byte, we pass it as padding... to pass the bytes
	// one by one
	// At this point I am not exactly sure how this works other than it works!
	outputBytes := append(bytesToPad, padding...)

	return outputBytes
}

// UnpadPKCS7 removes PKCS7 padding from []byte if any
// Reads the last byte, then reads that many bytes. If they are all the same
// value then we know padding is correct and we will remove it, otherwise error.
// Params:
//      paddedBytes: []byte padded input
//
// Return: []byte unpadded input and error if any
func UnpadPKCS7(paddedBytes []byte) ([]byte, error) {

	paddedLength := len(paddedBytes)

	// Read the last byte
	padding := paddedBytes[paddedLength-1]
	paddingLength := int(padding)

	// Check if we even have enough bytes
	if paddedLength < paddingLength {
		return nil, errors.New("input is too small to be padded!")
	}

	// Read last n bytes
	for i := 0; i < paddingLength; i++ {
		if paddedBytes[paddedLength-1-i] != padding {
			return nil, fmt.Errorf("wrong padding at byte %d."+
				"\nexpected %x but got %x.",
				i, padding, paddedBytes[paddedLength-1-i])
		}
	}

	return paddedBytes[:paddedLength-paddingLength], nil
}

// DecryptCBC decrypts []byte using AES-CBC
// Params:
//      ciphertext: []byte - encrypted data
//      key: []byte - should be 16 bytes
//      iv : []byte - Initialization Vector, should be 16 bytes
//
// Returns: []byte - decrypted string and error if any
func DecryptCBC(ciphertext, key, iv []byte) ([]byte, error) {

	// 1. Check if ciphertext is a multiple of 16
	if len(ciphertext)%16 != 0 {
		return nil, fmt.Errorf("ciphertext is %d bytes which is not "+
			"a multiple of 16.",
			len(ciphertext))
	}

	// 2. Check if IV and 16 are of same length
	if len(iv) != 16 {
		return nil, fmt.Errorf("IV has wrong length.\nexpected %d, got %d",
			16, len(iv))
	}

	// 2.5 Check if key and 16 are of same length
	if len(key) != 16 {
		return nil, fmt.Errorf("key has wrong length.\nexpected %d, got %d",
			16, len(key))
	}

	// 3. Split the ciphertext into 16 byte blocks
	blocks := SplitBytes(ciphertext, 16)

	// 4.  For each block
	// https://upload.wikimedia.org/wikipedia/commons/2/2a/CBC_decryption.svg

	// 4.1 DecryptECB the block
	// 4.2 XOR with IV
	// 4.3 store plaintext
	// 4.4 IV := block (old ciphertext)

	var plaintext []byte

	for _, block := range blocks {
		// 4.1 DecryptECB the block
		decryptedBlock, err := DecryptECB(block, key)

		// Check if it was decrypted correctly
		if err != nil {
			return nil, err
		}

		// 4.2 XOR with IV
		decryptedBlock = XOR(decryptedBlock, iv)

		// 4.3 store plaintext
		plaintext = append(plaintext, decryptedBlock...)

		// 4.4 IV := block (old ciphertext)
		iv = block
	}

	return plaintext, nil
}

// EncryptCBC encrypts []byte using AES-CBC
// Params:
//      plaintext: []byte
//      key: []byte - should be 16 bytes
//      iv : []byte - Initialization Vector, should be 16 bytes
//
// Returns: []byte - encrypted string and error if any
func EncryptCBC(plaintext, key, iv []byte) ([]byte, error) {

	// 1. Check if ciphertext is a multiple of 16
	if len(plaintext)%16 != 0 {
		return nil, fmt.Errorf("plaintext is %d bytes which is not "+
			"a multiple of 16.", len(plaintext))
	}

	// 2. Check if IV and 16 are of same length
	if len(iv) != 16 {
		return nil, fmt.Errorf("IV has wrong length.\nexpected %d, got %d",
			16, len(iv))
	}

	// 2.5 Check if key and 16 are of same length
	if len(key) != 16 {
		return nil, fmt.Errorf("key has wrong length.\nexpected %d, got %d",
			16, len(key))
	}

	// 3. Split the plaintext into 16 byte blocks
	blocks := SplitBytes(plaintext, 16)

	// 4.  For each block
	// https://upload.wikimedia.org/wikipedia/commons/8/80/CBC_encryption.svg

	// 4.1 XOR with IV
	// 4.2 EncryptECB the block
	// 4.3 store ciphertext
	// 4.4 IV := ciphertext

	var ciphertext []byte

	for _, block := range blocks {

		// 4.1 XOR with IV
		encryptedBlock := XOR(block, iv)

		// 4.2 EncryptECB the block
		encryptedBlock, err := EncryptECB(encryptedBlock, key)
		if err != nil {
			return nil, err
		}

		// 4.3 store ciphertext
		ciphertext = append(ciphertext, encryptedBlock...)

		// 4.4 IV := encryptedBlock
		iv = encryptedBlock
	}

	return ciphertext, nil
}

// NSARand returns an NSA sponsored random number generator seeded by timestamp
// Powered by math/rand, don't use for anything important
//
// Return: *rand.Rand
func NSARand() *rand.Rand {

	// Need to wait a bit between grabbing random bytes otherwise the output
	// from different applications is the same if done back to back
	// Same happens on https://play.golang.org/p/gjI3kNgZ4l
	time.Sleep(1 * time.Millisecond)

	// Create a seed
	seed := rand.NewSource(time.Now().UnixNano())
	// Seed the RNG and return
	return rand.New(seed)
}

// RandomBytes returns a []byte with n "random" bytes
// Powered by math/rand, don't use for anything important
// Params:
//      n: int - number o random bytes to return
//
// Return: []byte containing random bytes
func RandomBytes(n int) []byte {

	backdoored := NSARand()

	randomBytes := make([]byte, n)
	backdoored.Read(randomBytes)

	return randomBytes
}

// RandomIntRange returns a "random" int in [lower, upper)
// Powered by math/rand, don't use for anything important
// Params:
//      lower: int - lower range
//      upper: int - upper range
//
// Return: int - "random" between [lower, upper)
func RandomIntRange(lower, upper int) int {

	backdoored := NSARand()
	return backdoored.Intn(upper-lower) + lower
}

// EncryptionOracle encrypts input with random key according to cryptopals
// challenge 11 requirements:
//      encryption: AES
//      key: random
//      5-10 bytes added to the beginning or the end of input
//      ECB 50% of the time and CBC the rest with a random IV
//
// Params:
//      plaintext: []byte to be encrypted
//
// Return: []byte ciphertext
func EncryptionOracle(plaintext []byte) []byte {

	// Generate a random key
	key := RandomBytes(16)

	// Bytes to add to start and end
	beforeBytes := RandomBytes(RandomIntRange(5, 10))
	afterBytes := RandomBytes(RandomIntRange(5, 10))

	plaintext = append(beforeBytes, plaintext...)
	plaintext = append(plaintext, afterBytes...)

	plaintext = PadPKCS7(plaintext, 16)

	var encrypted []byte
	// Choose ECB or CBC
	if mode := RandomIntRange(0, 2); mode > 0 {
		// ECB
		// fmt.Println("ECB")
		enc, err := EncryptECB(plaintext, key)
		if err != nil {
			panic(err)
		}
		encrypted = enc
	} else {
		// CBC
		// fmt.Println("CBC")
		iv := RandomBytes(16)
		enc, err := EncryptCBC(plaintext, key, iv)
		if err != nil {
			panic(err)
		}
		encrypted = enc
	}

	return encrypted
}

// ECBOracle12 appends the target text to our input and encrypts it in ECB mode
// with a constant key for challenge 12
// Params:
//      input: []byte containing our input
//
// Return: []byte ciphertext and errors if any
func ECBOracle12(input []byte) ([]byte, error) {

	ch12Key := []byte("0123456789012345")

	unknown := "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg" +
		"aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq" +
		"dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg" +
		"YnkK"

	// Decode unknown bytes
	unknownBytes, err := B64DecodeStrToByte(unknown)
	if err != nil {
		return nil, err
	}

	// Append our input to unknown bytes
	plaintext := append(input, unknownBytes...)

	// Pad them all to blocksize
	plaintext = PadPKCS7(plaintext, 16)

	// ECB encrypt with constant key
	enc, err := EncryptECB(plaintext, ch12Key)
	if err != nil {
		return nil, err
	}

	return enc, nil
}

// QueryToJSON converts a query string into JSON
// Params:
//      queryString: string - key1=value1&key2=value2
//
// Return: []byte - JSON object with the parsed query string and error
func QueryToJSON(queryString string) ([]byte, error) {

	parsedQuery, err := url.ParseQuery(queryString)
	if err != nil {
		return nil, err
	}

	jsonString, err := json.Marshal(parsedQuery)
	if err != nil {
		return nil, err
	}

	return jsonString, nil
}

// ProfileFor13 creates a query string URL based on user's email for challenge 13
// profile_for("foo@bar.com") should return "email=foo@bar.com&uid=10&role=user"
// Params:
//      email: string - user's email
//
// Return: string containing the query string
func ProfileFor13(email string) string {

	value := url.Values{}
	value.Add("email", email)

	// Using value.Add will change the sequence and sort the attributes
	// meaning it will be role=user&uid=10
	// value.Add("uid", "10")
	// value.Add("role", "user")

	encoded := value.Encode()

	encoded, _ = url.QueryUnescape(encoded)

	return encoded + "&uid=10&role=user"
}

// EncryptProfile13 creates a userprofile based on their email using ProfileFor13
// and then encrypts it in ECB mode using a static AES key for challenge 13
// Params:
//      email: string - user's email and error if applicable
//
// Return: encryptedProfile - []byte
func EncryptProfile13(email string) ([]byte, error) {

	ch13Key := []byte("0123456789012345")

	// Create profile
	profile := ProfileFor13(email)
	// Convert to []byte
	profileBytes := []byte(profile)
	// Pad it to blocksize
	profileBytes = PadPKCS7(profileBytes, 16)

	// encryptedProfile, err := EncryptECB(profileBytes, ch13Key)
	// if err != nil {
	//     return nil, err
	// }

	// return encryptedProfile, nil

	// Save a few instructions and look kewl
	return EncryptECB(profileBytes, ch13Key)
}

// DecryptProfile13 decrypts a userprofile, parses the query string and returns JSON
// Params:
//      encryptedProfile: []byte encrypted bytes
//
// Return: profile: string - JSON object with user profile and errors if any
func DecryptProfile13(encryptedProfile []byte) (string, error) {

	ch13Key := []byte("0123456789012345")

	// Check if encryptedProfile length is a multiple of 16
	if len(encryptedProfile)%16 != 0 {
		return "", fmt.Errorf("input length %d is not a multiple of 16\n",
			len(encryptedProfile))
	}

	decryptedProfile, err := DecryptECB(encryptedProfile, ch13Key)
	if err != nil {
		return "", err
	}

	return string(decryptedProfile), err

}

// ECBOracle14 prepends a number of random bytes to our input, appends it with
// the target text and encrypts it in ECB with a constant key for challenge 14
// Params:
//      input: []byte containing our input
//
// Return: []byte ciphertext and errors if any
func ECBOracle14(input []byte) ([]byte, error) {

	key := []byte("0123456789012345")

	unknown := "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg" +
		"aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq" +
		"dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg" +
		"YnkK"

	// Decode unknown bytes
	unknownBytes, err := B64DecodeStrToByte(unknown)
	if err != nil {
		return nil, err
	}

	// THE LENGTH OF PREFIX IS UNKNOWN BUT CONSTANT
	// Intially I was generating a random-length prefix which makes solving
	// almost impossible
	beforeBytes := RandomBytes(25)

	plaintext := append(beforeBytes, input...)

	// fmt.Println(len(plaintext))

	// Append our input to unknown bytes
	plaintext = append(plaintext, unknownBytes...)

	// Pad them all to blocksize
	plaintext = PadPKCS7(plaintext, 16)

	// ECB encrypt with constant key
	enc, err := EncryptECB(plaintext, key)
	if err != nil {
		return nil, err
	}

	return enc, nil
}

// CBCEncrypt16 prepends and appends user input with two strings, uses PKCS7 to
// pad them and finally encrypt everything with unknown but static key, IV
// using AES-CBC for challenge 16
// Params:
//      input: string - user input
//
// Return: ciphertext: []byte containing encrypted text
func CBCEncrypt16(input string) []byte {

	key := []byte("0123456789012345")
	iv := []byte("AnimeWasAMistake")

	preString := "comment1=cooking%20MCs;userdata="
	postString := ";comment2=%20like%20a%20pound%20of%20bacon"

	newString := preString + input + postString

	newBytes := []byte(newString)
	paddedBytes := PadPKCS7(newBytes, 16)

	enc, err := EncryptCBC(paddedBytes, key, iv)
	if err != nil {
		panic(err)
	}

	return enc
}

// CBCDecrypt16 decrypts the input and returns true if it contains ";admin=true"
// otherwise returns false
// Params:
//      encrypted: []byte - encrypted bytes
//
// Return: bool - true if decrypted string contains ";admin=true"
func CBCDecrypt16(input []byte) bool {

	key := []byte("0123456789012345")
	iv := []byte("AnimeWasAMistake")

	dec, err := DecryptCBC(input, key, iv)
	if err != nil {
		return false
	}

	return strings.Contains(string(dec), ";admin=true")
}
