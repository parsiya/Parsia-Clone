package urlshort

import (
	"net/http"

	yaml2 "gopkg.in/yaml.v2"
)

// MapHandler will return an http.HandlerFunc (which also
// implements http.Handler) that will attempt to map any
// paths (keys in the map) to their corresponding URL (values
// that each key in the map points to, in string format).
// If the path is not provided in the map, then the fallback
// http.Handler will be called instead.
func MapHandler(pathsToUrls map[string]string, fallback http.Handler) http.HandlerFunc {
	//	TODO: Implement this...
	// Read this: https://medium.com/@matryer/the-http-handler-wrapper-technique-in-golang-updated-bc7fbcffa702
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Now we need to get the request URL from r
		// See here for an example from the docs
		// https://golang.org/pkg/net/http/
		p := r.URL.Path
		// Check if p exists in the map, if key does not exist in map exists
		// will be nil
		if redirect, exists := pathsToUrls[p]; exists {
			// redirect with a 302.
			http.Redirect(w, r, redirect, http.StatusFound)
			return
		}
		// If it's not found, call fallback.
		fallback.ServeHTTP(w, r)
	})

}

// YAMLHandler will parse the provided YAML and then return
// an http.HandlerFunc (which also implements http.Handler)
// that will attempt to map any paths to their corresponding
// URL. If the path is not provided in the YAML, then the
// fallback http.Handler will be called instead.
//
// YAML is expected to be in the format:
//
//     - path: /some-path
//       url: https://www.some-url.com/demo
//
// The only errors that can be returned all related to having
// invalid YAML data.
//
// See MapHandler to create a similar http.HandlerFunc via
// a mapping of paths to urls.
func YAMLHandler(yml []byte, fallback http.Handler) (http.HandlerFunc, error) {

	pathToUrls, err := YamlToMap(yml)
	if err != nil {
		return nil, err
	}

	return MapHandler(pathToUrls, fallback), nil
}

// PathObject contains a path/url combo.
type PathObject struct {
	Path string `yaml:"path"`
	URL  string `yaml:"url"`
}

// YamlToMap converts a yaml file of PathObjects to a map consumable by MapHandler.
func   (yml []byte) (map[string]string, error) {
	// https://godoc.org/gopkg.in/yaml.v2

	// Read yaml from bytes
	var paths []PathObject
	err := yaml2.Unmarshal(yml, &paths)
	if err != nil {
		return nil, err
	}
	// Convert to map
	pathsToUrls := make(map[string]string)
	for _, p := range paths {
		pathsToUrls[p.Path] = p.URL
	}
	return pathsToUrls, nil
}
