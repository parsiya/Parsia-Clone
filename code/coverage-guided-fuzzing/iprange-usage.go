package main

import (
	"log"

	"github.com/malfunkt/iprange"
)

func main() {
	list, err := iprange.ParseList("10.0.0.5-10, 192.168.10.0/24")
	if err != nil {
		log.Printf("error: %s", err)
	}
	log.Printf("%+v", list)

	rng := list.Expand()
	log.Printf("%s", rng)
}
