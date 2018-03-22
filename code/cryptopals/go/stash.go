import (
	"math"
	"sort"
)

// Code that is not used (yet)

// StrToByte converts string to []byte
// Params:
//      input: string to be converted to bytes
//
// Return: Byte array containing bytes from the string
func StrToByte(inputString string) []byte {
	return []byte(inputString)
}

// isUppercase returns true if input's ASCII-Hex code is
// between 0x41 "A" and 0x5A "Z" (inclusive)
// Params:
//      char: byte char to be evaluated
//
// Return: true if char is uppercase and false if not
func isUppercase(char byte) bool {
	return ((0x41 <= char) && (char <= 0x5A))
}

// ByteToStr converts []byte to string
// Params:
//      inputBytes: []byte to be converted to string
//
// Return: string converted from []byte
// Note: This will stop at the first null-byte
func ByteToStr(inputBytes []byte) string {
	return string(inputBytes[:])
}

// BytesToLowerCase converts a []byte to lowercase.
// We could probably do it by converting it to string, lowercase and then back.
// But muh reverse-engineering credz!!1!
// Capital letters are between 0x41<= byte <=0x5A
// Capital to small in ASCII-Hex can be done by adding 0x20
// E.g. "A" is 0x41, "a" is 0x61 (0x41 + 0x20)
// Params:
//      inputBytes: []byte containing string
//
// Return: []byte lowercase string
func bytesToLowerCase(inputBytes []byte) []byte {

	mixedcaseBytes := make([]byte, len(inputBytes))

	for i := 0; i < len(inputBytes); i++ {
		if uppercase := isUppercase(inputBytes[i]); uppercase {
			// Convert to lowercase
			mixedcaseBytes[i] = inputBytes[i] + 0x20
		}
	}
	return mixedcaseBytes
}

// GetLetterCount returns a struct containing letter count of a-z and space.
// Params:
//      textBytes: []byte containing the input string
// Return: A map[string]int where key is character and value is count
func getLetterCount(textBytes []byte) map[string]int {

	counts := make(map[string]int)

	// Convert to lowercase for counting
	lowercase := bytesToLowerCase(textBytes)
	for _, char := range lowercase {
		// If character is space or [a-z]
		if (char == 0x20) || ((0x61 <= char) && (char <= 0x7A)) {
			counts[string(char)] += 1
		}
	}
	return counts
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

// letterFreqScore calculates a score based on English letter frequency.
// Our sentences are pretty short in this challenge so I am not sure how it
// will work out.
// The score is sum of the difference between actual and expected letter count
// for each letter [a-z] and space (everything is converted to lowercase in the
// GetLetterCount function before processing). LOWER IS BETTER.
// Params:
//      textBytes: []byte containing the string in ASCII-Hex
//
// Return: float64 score - because math.Abs only works for float64
// I don't wanna say it but lol no math for int??
func letterFreqScore(textBytes []byte) float64 {
	textLen := float64(len(textBytes))

	letterCount := getLetterCount(textBytes)

	score := 0.0

	score += math.Abs((frequency[" "] * textLen) - float64(letterCount[" "]))

	for i := 0x61; i <= 0x7A; i++ {
		expectedCount := frequency[string(i)] * textLen
		score += math.Abs(expectedCount - float64(letterCount[string(i)]))
	}

	return score
}

// Struct to hold the results
type Result struct {
	Key            byte
	PrintableScore int
	Plaintext      []byte
	EnglishScore   float64
}

// BreakSingleByteXOR attempts to break single byte XOR encryption.
// It uses LetterFreqScore to find the one with the lowest score and
// returns the struct.
// Params:
//      ciphertext: []byte containing single-byte XOR encrypted string.
//
// Return: genericpals.Results
func BreakSingleByteXOR(ciphertext []byte) Result {

	results := make([]Result, 0x100)

	for key := 0; key < 0x100; key++ {

		plaintext := SingleByteXOR(ciphertext, byte(key))

		results[key].Plaintext = plaintext
		results[key].Key = byte(key)
		results[key].PrintableScore = printableEnglish(plaintext)
		results[key].EnglishScore = letterFreqScore(plaintext)
	}

	// Sorting the array using sort.Slice
	// https://stackoverflow.com/a/42872183

	// Sort
	sort.Slice(results[:], func(i, j int) bool {
		return results[i].EnglishScore < results[j].EnglishScore
	})

	return results[0]
}

// Evaluate compares output with expected output and returns pass or fail along
// with other information.
// Params:
//      result  : What we got
//      expected: What we should get
//
// Return: String containing pass/fail + information
// func Evaluate(result interface{}, expected interface{}) bool {
//

//     eval := false
//     val1 := reflect.ValueOf(result)
//     val2 := reflect.ValueOf(expected)

//     if (val1.Kind() != val2.Kind()) {
//         return eval
//     }

//     switch val1.Kind() {
//         case relfect.
//     }

//     switch t1 := result.(type) {
//     case []uint8:
//         eval = bytes.Equal(result, expected)
//     default:
//         eval = (result == expected)
//     }

//     return eval

// if result.(T) != expected.(T) {
//     return "", fmt.Errorf("Different types passed." +
//                               "result type %T != %T expected type",
//                                result, expected)
// } else {
//     eval := false
//     switch t := result.(type) {
//     case []byte:
//         eval = bytes.Equal(result, expected)
//     default:
//         eval = (result == expected)
//     }

//     errorString := ""
//     if eval {
//         errorString = fmt.Printf("Passed! Result is %v", result)
//     } else {
//         errorString = fmt.Printf("Failed!\nGot %v\nWanted %v",
//                                  result, expected)
//     }

//     return errorString, nil
// }

// }