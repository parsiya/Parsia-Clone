package main

import (
	"encoding/csv"
	"flag"
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/olekukonko/tablewriter"
)

var fileName string
var timeLimit int

// Question contains a Q/A pair.
type Question struct {
	Q string
	A string
}

func init() {
	flag.StringVar(&fileName, "q", "problems.csv", "csv file with questions")
	flag.IntVar(&timeLimit, "t", 30, "timelimit in seconds")
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
	fmt.Println("Press Enter when you are ready to start.")
	fmt.Printf("You have %d seconds.", timeLimit)
	fmt.Scanln()

	correct := 0

	// Use a timer, see https://gobyexample.com/timers.
	ti := time.NewTimer(time.Duration(timeLimit) * time.Second)

	go func() {
		for _, q := range questions {
			fmt.Printf("%s? ", q.Q)
			var answer string
			fmt.Scanln(&answer)
			fmt.Println()
			if answer == q.A {
				correct++
			}
		}

		// Reset the timer if we are done with questions.
		// ti.Stop() does not send anything to the channel.
		ti.Reset(0)
	}()

	// Wait for timer to expire or get cancelled.
	<-ti.C

	fmt.Println()
	table := tablewriter.NewWriter(os.Stdout)
	table.SetHeader([]string{"Correct answers", "Total questions"})
	table.Append([]string{strconv.Itoa(correct), strconv.Itoa(len(qs))})
	table.Render()
}
