package main

import (
	"flag"
	"fmt"
)

var fileName string
var timeLimit int
var shuffle bool

func init() {
	flag.StringVar(&fileName, "q", "problems.csv", "csv file with questions")
	flag.IntVar(&timeLimit, "t", 30, "timelimit in seconds")
	flag.BoolVar(&shuffle, "shuffle", false, "shuffles question order")
	flag.Parse()
}

func main() {

	var exam Exam
	if err := exam.SetTimeLimit(timeLimit); err != nil {
		panic(err)
	}

	if err := exam.Populate(fileName); err != nil {
		panic(err)
	}

	// File has been read, time to start asking questions.
	fmt.Println("Time for the quiz. Answer each question and press Enter.")
	fmt.Println("Press Enter when you are ready to start.")
	fmt.Printf("You have %d seconds.", timeLimit)
	fmt.Scanln()

	exam.Start(shuffle)

	fmt.Println("\nTime's up!")
	fmt.Println(exam.Result())
}
