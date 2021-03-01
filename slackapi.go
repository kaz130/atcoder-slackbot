package main

import (
	"fmt"
	"bytes"
	"io/ioutil"
	"net/http"
	"encoding/json"
)

type SlackClient struct {
	token	string
}


type MessageArguments struct {
	Channel	string	`json:"channel"`
	Text	string	`json:"text"`
}

func (slack *SlackClient) PostMessage (message MessageArguments) {
	methodURL := "https://slack.com/api/chat.postMessage"

	jsonStr, _ := json.Marshal(message)
	req, err := http.NewRequest("POST", methodURL, bytes.NewBuffer(jsonStr))
	req.Header.Add("Authorization", "Bearer " + slack.token)
	req.Header.Add("Content-type", "application/json")

	client := new(http.Client)
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	fmt.Println("response Status:", resp.Status)
	fmt.Println("response Headers:", resp.Header)
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("response Body:", string(body))
}

