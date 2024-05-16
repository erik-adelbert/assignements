package main

import (
	"encoding/json"
	"errors"
	"net/http"
)

type ServerError interface {
	// ServerError returns an HTTP status code and an API-safe error message.
	ServerError() (int, string)
}

type privServerError struct {
	status int
	msg    string
}

func (e privServerError) Error() string {
	return e.msg
}

func (e privServerError) ServerError() (int, string) {
	return e.status, e.msg
}

var (
	InvalidId   = &privServerError{status: http.StatusBadRequest, msg: "invalid user id"}
	ErrNotFound = &privServerError{status: http.StatusNotFound, msg: "user id not found"}
)

type privateWrappedError struct {
	error
	priv *privServerError
}

func (e privateWrappedError) Is(err error) bool {
	return e.priv == err
}

func (e privateWrappedError) APIError() (int, string) {
	return e.priv.ServerError()
}

func WrapError(err error, priv *privServerError) error {
	return privateWrappedError{error: err, priv: priv}
}

func JSONError(w http.ResponseWriter, status int, msg string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)

	response := map[string]string{"error": msg}
	json.NewEncoder(w).Encode(response)
}

func JSONHandleError(w http.ResponseWriter, err error) {
	var serverErr ServerError
	if errors.As(err, &serverErr) {
		status, msg := serverErr.ServerError()
		JSONError(w, status, msg)
	} else {
		JSONError(w, http.StatusInternalServerError, "internal error")
	}
}
