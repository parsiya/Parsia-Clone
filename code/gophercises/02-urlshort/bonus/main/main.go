package main

import (
	"flag"
	"fmt"
	"net/http"

	urlshort "github.com/parsiya/Parsia-Clone/code/gophercises/02-urlshort/bonus"
)

var yamlFile string
var jsonFile string

func init() {
	flag.StringVar(&yamlFile, "yaml", "", "yaml file containing paths")
	flag.StringVar(&jsonFile, "json", "", "json file containing paths")

	flag.Parse()
}

func main() {
	mux := defaultMux()

	// Build the MapHandler using the mux as the fallback
	pathsToUrls := map[string]string{
		"/urlshort-godoc": "https://godoc.org/github.com/gophercises/urlshort",
		"/yaml-godoc":     "https://godoc.org/gopkg.in/yaml.v2",
	}
	mapHandler := urlshort.MapHandler(pathsToUrls, mux)

	// Build the YAMLHandler using the mapHandler as the
	// fallback

	var yaml []byte

	if jsonFile == "" {
		// Populate yaml from file (or default if it does not exist)
		yaml = urlshort.ParseYaml(yamlFile)
	} else {
		// Populate yaml from JSON file
		yaml = urlshort.ParseJSON(jsonFile)
	}

	yamlHandler, err := urlshort.YAMLHandler(yaml, mapHandler)
	if err != nil {
		panic(err)
	}
	fmt.Println("Starting the server on :8080")
	http.ListenAndServe(":8080", yamlHandler)
}

func defaultMux() *http.ServeMux {
	mux := http.NewServeMux()
	mux.HandleFunc("/", hello)
	return mux
}

func hello(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Hello, world!")
}
