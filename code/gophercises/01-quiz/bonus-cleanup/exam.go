// LOL Object Oriented.
package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/olekukonko/tablewriter"
)

// Problem contains a Q/A pair.
type problem struct {
	Question string
	Answer   string
}

// Exam contains a list of questions, a time limit, and # of correct answers.
type Exam struct {
	problems       []problem
	timeLimit      time.Duration
	correctAnswers int
}

// Populate reads questions from a csv file and adds them to the exam.
func (e *Exam) Populate(questionFile string) error {

	// Open csv file.
	f, err := os.Open(questionFile)
	if err != nil {
		return fmt.Errorf("error opening questions file: %v", err)
	}

	// Read csv file.
	cr := csv.NewReader(f)
	qs, err := cr.ReadAll()
	if err != nil {
		return fmt.Errorf("Error parsing questions: %v", err)
	}

	for _, v := range qs {
		var p problem
		p.Question = v[0]
		p.Answer = v[1]
		// Append is slow, but we do not have many questions.
		e.problems = append(e.problems, p)
	}

	return nil
}

// SetTimeLimit sets the timelimit for the exam.
func (e *Exam) SetTimeLimit(t int) error {
	if t == 0 {
		return fmt.Errorf("invalid time limit, got %v", t)
	}
	e.timeLimit = time.Duration(t) * time.Second
	return nil
}

// Start starts the exam. Exam will end if we run out of questions or time.
// If shuffle is true, question order will be randomized.
func (e *Exam) Start(shuffle bool) {

	correct := 0

	fmt.Println(e.timeLimit)

	// Use a timer, see https://gobyexample.com/timers.
	ti := time.NewTimer(e.timeLimit)

	if shuffle {
		e.Shuffle()
	}

	go func() {
		for _, p := range e.problems {
			fmt.Printf("%s? ", p.Question)
			var answer string
			fmt.Scanln(&answer) // ignoring the error here.
			fmt.Println()
			// Trim space from answer.
			answer = strings.Trim(answer, " ")
			// Compare answers in lowercase.
			if strings.ToLower(answer) == strings.ToLower(p.Answer) {
				correct++
			}
		}

		// Reset the timer if we are done with questions.
		// ti.Stop() does not send anything to the channel.
		ti.Reset(0)
	}()

	// Wait for timer to expire or get cancelled.
	<-ti.C

	// Update correct answers.
	e.correctAnswers = correct
}

// Result returns the exam result table in a string.
func (e Exam) Result() string {

	buf := bytes.NewBufferString("\n")
	table := tablewriter.NewWriter(buf)
	table.SetHeader([]string{"Correct answers", "Total questions"})
	table.Append([]string{strconv.Itoa(e.correctAnswers), strconv.Itoa(len(e.problems))})
	table.Render()

	return buf.String()
}

// Shuffle, shuffles the order of questions in a non-cryptographically secure way.
// Based on https://www.calhoun.io/how-to-shuffle-arrays-and-slices-in-go/.
func (e *Exam) Shuffle() {
	rnd := rand.New(rand.NewSource(time.Now().Unix()))
	for n := len(e.problems); n > 0; n-- {
		i := rnd.Intn(n)
		e.problems[n-1], e.problems[i] = e.problems[i], e.problems[n-1]
	}
}
