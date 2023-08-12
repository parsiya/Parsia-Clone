---
draft: false
toc: true
comments: false
categories:
- Abandoned Research
tags:
- semgrep
title: "Semgrep Output Processing in Go"
wip: false
snippet: "Adventures in Converting Semgrep Output JSON Schema to Go Structs"

---

This is something I wrote in November 2022 when I was trying to convert the
JSON Schema for Semgrep's output to Go structs. Things have changed since then
and I think gojsonschema works correctly now.

# Draft 2020-12
Located at https://github.com/returntocorp/semgrep-interfaces/blob/main/semgrep_output_v0.jsonschema.

This draft is too advanced so most libraries cannot parse it.

[atombender/go-jsonschema](https://github.com/atombender/go-jsonschema) CAN get something IF we use the master branch (and not the latest tagged version).

The lastest tagged version gets this error:

```
$ go install github.com/atombender/go-jsonschema/cmd/gojsonschema@mlatest

$ gojsonschema -p main -o semgrep-result.go --verbose semgrep_output_v0.jsonschema
gojsonschema: Loading semgrep_output_v0.jsonschema
gojsonschema: Failed: error parsing from file semgrep_output_v0.jsonschema: json: cannot unmarshal bool into Go struct field Type.definitions.oneOf.items of type schemas.Type
```

But the latest commit from master does more:

```
$ go install github.com/atombender/go-jsonschema/cmd/gojsonschema@master

$ gojsonschema -p main -o semgrep_result.go --verbose semgrep_output_v0.jsonschema
gojsonschema: Loading semgrep_output_v0.jsonschema
gojsonschema: Warning: Property has multiple types; will be represented as interface{} with no validation
gojsonschema: Warning: Property has multiple types; will be represented as interface{} with no validation
gojsonschema: Warning: Property has multiple types; will be represented as interface{} with no validation
gojsonschema: Warning: Multiple types map to the name "CliMatchExtra"; declaring duplicate as "CliMatchExtra_1" instead
gojsonschema: Warning: Cycle detected; must wrap type MatchingExplanation in pointer
gojsonschema: Warning: Multiple types map to the name "CoreMatchExtra"; declaring duplicate as "CoreMatchExtra_1" instead
gojsonschema: Writing semgrep_result.go
```

See `go-jsonschema_semgrep_result.go` file below. See how problematic stuff like `CoreErrorKind` are handwaved as `interface{}` (line 229).

Everything else returns a similar error. Apparently, it's because they might not support the draft 2020-12 versions.

For example, [a-h/generate](https://github.com/a-h/generate). Getting this to install is tricky, because the instructions use `go get` which has been deprecated for quite some time.

```
$ git clone https://github.com/a-h/generate --depth=1
$ cd generate
# the mod name is not important, you can use whatever you want
$ go mod init github.com/a-h/generate
$ go mod tidy
$ go get github.com/a-h/generate
$ make
```

Now, we have the `schema-generate` executable here.

```
$ ./schema-generate -p main -o ../generate.go ../semgrep_output_v0.jsonschema
the JSON type 'bool' cannot be converted into the Go 'Schema' type on struct 'Schema', field 'Definitions.OneOf.Items'. See input file ../semgrep_output_v0.jsonschema line 128, character 26
```

Seems like our issue is about implementing `OneOf.Items`. One of the pull requests mention fixing it and it didn't work either.

```
$ git clone https://github.com/lustefaniak/generate/ generate-oneoff --depth=1 -b optional-one-off
$ cd generate-oneoff
# the mod name is not important, you can use whatever you want
$ go mod init github.com/lustefaniak/generate
$ go mod tidy
$ make
```

https://git.sr.ht/~emersion/go-jsonschema supposedly supports Draft 2020-12 but just generates this useless struct (for both versions):

```go
package main

type Root map[string]interface{}
```

# Draft-07
Martin kindly provided a version of the JSONSchema in the Draft-07 version:
https://github.com/returntocorp/semgrep-interfaces/blob/mj-jsonschema-2019/semgrep_output_v0.jsonschema-draft-07

I could get it to work was in [https://app.quicktype.io/](https://app.quicktype.io/). It omitted some structs.

You can see the result in the `semgrep_results_quicktype-io.go` file below.

Everything else still had issues (even the master version of `gojsonschema` that worked with the 2020-12 version above.

```
$ ./schema-generate -p main -o ../generate_3.go ../semgrep_output_v0.jsonschema-draft-07
the JSON type 'array' cannot be converted into the Go 'Schema' type on struct 'Schema', field 'Definitions.OneOf.Items'. See input file ../semgrep_output_v0.jsonschema-draft-07 line 130, character 1
```

Which is:

```json
    "core_error_kind": {
      "oneOf": [
        { "const": "Lexical error" },
        { "const": "Syntax error" },
        { "const": "Other syntax error" },
        { "const": "AST builder error" },
        { "const": "Rule parse error" },
        {
          "type": "array",
          "minItems": 2,
          "additionalItems": false,
          "items": [ // <--- HERE
            { "const": "Pattern parse error" },
            { "type": "array", "items": { "type": "string" } }
          ]
```

Anyways, this is where I rage quit. I think I have enough structs to do what I want because I don't care about the errors at this point.