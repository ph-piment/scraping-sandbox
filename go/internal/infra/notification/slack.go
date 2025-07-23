package notification

import (
	"fmt"

	"github.com/slack-go/slack"
)

//go:generate go run github.com/maxbrunsfeld/counterfeiter/v6 -generate

//counterfeiter:generate -o ../../../test/mocks/notificationfakes . Slack

type Slack interface {
	Notify(channelID, message string) error
}

type client struct {
	api *slack.Client
}

func NewSlack(token string) Slack {
	return &client{
		api: slack.New(token),
	}
}

func (c *client) Notify(channelID, message string) error {
	_, _, err := c.api.PostMessage(channelID, slack.MsgOptionText(message, true))
	if err != nil {
		return fmt.Errorf("failed to send Slack message: %w", err)
	}
	return nil
}
