// Contains different utilities used by main.go

package urlshort

import (
	"encoding/json"
	"fmt"
	"io/ioutil"

	yaml2 "gopkg.in/yaml.v2"
)

var hardcoded = []byte(`
- path: /urlshort
  url: https://github.com/gophercises/urlshort
- path: /urlshort-final
  url: https://github.com/gophercises/urlshort/tree/solution
`)

// ParseYaml reads a yaml file and returns a []byte that can be consumed
// by YAMLHandler, if file does not exist or an error is encountered, hardcoded
// values are returned.
func ParseYaml(f string) []byte {

	yaml, err := ioutil.ReadFile(f)
	if err != nil {
		return hardcoded
	}
	return yaml
}

// ParseJSON reads a JSON file and returns a []byte that can be consumed by
// by YAMLHandler, if file does not exist or an error is encountered, hardcoded
// values are returned.
func ParseJSON(f string) []byte {

	var paths []PathObject

	js, err := ioutil.ReadFile(f)
	if err != nil {
		return hardcoded
	}

	err = json.Unmarshal(js, &paths)
	if err != nil {
		fmt.Println("json unmarshal error")
		return hardcoded
	}

	// Obviously this is not optimal but we do not have to modify YAMLHandler
	// in main.go.
	y, err := yaml2.Marshal(paths)
	if err != nil {
		fmt.Println("yaml marshall error")
		return hardcoded
	}
	return y
}
