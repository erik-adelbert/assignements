package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"strconv"
	"time"
)

type User struct {
	Id   int    `json:"id"`
	Name string `json:"name"`
}

const MaxUsers = 100

type UserService struct {
	db   map[int]*User
	nhit int

	cache map[int]*User
}

func NewUserService() *UserService {
	db := make(map[int]*User, MaxUsers)

	for i := range MaxUsers {
		// from User1 to User100
		db[i+1] = &User{
			Id:   i + 1,
			Name: fmt.Sprintf("User%d", i+1),
		}
	}

	return &UserService{
		db:    db,
		cache: make(map[int]*User, MaxUsers),
	}
}

func (s *UserService) cacheGet(id int) (*User, bool) {
	user, ok := s.cache[id]
	if !ok {
		return nil, false
	}
	return user, true
}

func (s *UserService) cacheSet(id int, user *User) error {
	s.cache[id] = user
	return nil
}

func (s *UserService) getUser(w http.ResponseWriter, r *http.Request) {
	idStr := r.URL.Query().Get("id")

	id, err := strconv.Atoi(idStr)
	if err != nil {
		err = WrapError(err, InvalidId)
		log.Printf("getUser: invalid user id: %v", err)
		JSONHandleError(w, err)
		return
	}

	user, ok := s.cacheGet(id)
	if !ok {
		// cache miss
		user, ok = s.db[id]
		time.Sleep(3 * time.Millisecond) // simulate DB roundtrip
		if !ok {
			err = WrapError(err, ErrNotFound)
			log.Printf("getUser: error fetching user: %v", err)
			JSONHandleError(w, err)
			return
		}
		s.cacheSet(id, user) // cache load
		s.nhit++
	}

	json.NewEncoder(w).Encode(user)
}

type AddressKey string

const serverAddr = "serverAddr"

func main() {
	ctx, cancel := context.WithCancel(context.Background())

	userService := NewUserService()

	router := http.NewServeMux()
	router.HandleFunc("/", getRoot)
	router.HandleFunc("/user/", userService.getUser)

	newMuxServer := func(a string) *http.Server {
		return &http.Server{
			Addr:    a,
			Handler: router,
			BaseContext: func(l net.Listener) context.Context {
				ctx = context.WithValue(ctx, AddressKey(serverAddr), l.Addr().String())
				return ctx
			},
		}
	}

	servers := []*http.Server{
		newMuxServer(":3333"),
		//newMuxServer(":4444"),
	}

	for i, s := range servers {
		go func(s *http.Server, i int) {
			err := s.ListenAndServe()
			switch {
			case errors.Is(err, http.ErrServerClosed):
				fmt.Printf("server %d is closed\n", i)
			case err != nil:
				fmt.Printf("server %d is not starting: %s\n", i, err)
			}
			cancel()
		}(s, i)
	}
	<-ctx.Done()
}

func getRoot(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	fmt.Printf("%s: got / request\n", ctx.Value(AddressKey(serverAddr)))

	if body, err := io.ReadAll(r.Body); err != nil {
		fmt.Printf(" could not read body: %s\n", err)
	} else {
		fmt.Printf(" body:\n%s\n", body)
	}

	vars := []string{"first", "second"}
	vals := make([]string, len(vars))

	fmt.Print(" vars: ")
	for i, v := range vars {
		if r.URL.Query().Has(v) {
			vals[i] = r.URL.Query().Get(v)
			fmt.Printf("%s = '%s' ", v, vals[i])
		}
	}
	fmt.Print("\n")

	io.WriteString(w, "This is a website!\n")
}
