package main

import (
	"log"
	"github.com/BurntSushi/toml"
)

type Config struct {
	Slack SlackConfig
}

type SlackConfig struct {
	Token string
	Channel string
}


func main() {
	var config Config
	_, err := toml.DecodeFile("config.toml", &config)
	if err != nil {
		log.Fatal(err)
	}

	slack := SlackClient{config.Slack.Token}
	message := MessageArguments{config.Slack.Channel, "test"}
	slack.PostMessage(message)
}


