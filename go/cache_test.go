package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
	"time"
)

const MaxRequest = 2000

func TestGetUser(t *testing.T) {
	s := NewUserService()
	ts := httptest.NewServer(http.HandlerFunc(s.getUser))

	nreq := MaxRequest

	var wg sync.WaitGroup

	wg.Add(nreq)
	for i := range nreq {
		// spawn nreq concurrent requests
		go func(i int) {
			defer wg.Done()

			id := 1 + i%100
			url := fmt.Sprintf("%s/?id=%d", ts.URL, id)
			resp, err := http.Get(url)
			if err != nil {
				t.Error(err)
			}
			defer resp.Body.Close()

			user := &User{}
			if err := json.NewDecoder(resp.Body).Decode(user); err != nil {
				t.Error(err)
			}

			fmt.Printf("%+v\n", user)
		}(i)
		time.Sleep(time.Millisecond)
	}
	wg.Wait()

	fmt.Println("******************************************************************************")
	fmt.Println()
	fmt.Println("hits on db:", s.nhit, "nreq:", nreq, "pressure:", float32(s.nhit)/float32(nreq))
	fmt.Println()
	fmt.Println("******************************************************************************")
}
