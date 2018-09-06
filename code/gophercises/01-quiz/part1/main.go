package main

import (
	"encoding/csv"
	"flag"
	"fmt"
	"os"
	"strconv"

	"github.com/olekukonko/tablewriter"
)

var fileName string

// Question contains a Q/A pair.
type Question struct {
	Q string
	A string
}

func init() {
	flag.StringVar(&fileName, "questions", "problems.csv", "csv file with questions")
	flag.Parse()
}

func main() {

	f, err := os.Open(fileName)
	if err != nil {
		panic(fmt.Errorf("error opening questions file: %v", err))
	}

	// Read csv file
	cr := csv.NewReader(f)
	qs, err := cr.ReadAll()
	if err != nil {
		panic(fmt.Errorf("Error parsing questions: %v", err))
	}

	questions := make([]Question, len(qs))

	for i, v := range qs {
		questions[i].Q = v[0]
		questions[i].A = v[1]
	}

	// File has been read, time to start asking questions.
	fmt.Println("Time for the quiz. Answer each question and press Enter.")
	correct := 0

	for _, q := range questions {
		fmt.Printf("%s? ", q.Q)
		var answer string
		fmt.Scanln(&answer)
		fmt.Println()
		if answer == q.A {
			correct++
		}
	}

	table := tablewriter.NewWriter(os.Stdout)
	table.SetHeader([]string{"Correct answers", "Total questions"})
	table.Append([]string{strconv.Itoa(correct), strconv.Itoa(len(qs))})
	table.Render()
}
