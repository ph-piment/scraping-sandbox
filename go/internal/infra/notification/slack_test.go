package notification_test

import (
	"errors"

	"scraping-sandbox/internal/infra/notification"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
	"github.com/slack-go/slack"
)

type fakeSlackPoster struct {
	CalledChannel string
	CalledOptions []slack.MsgOption
	ReturnError   error
}

func (f *fakeSlackPoster) PostMessage(channelID string, options ...slack.MsgOption) (string, string, error) {
	f.CalledChannel = channelID
	f.CalledOptions = options
	return "ts123", "ch123", f.ReturnError
}

var _ = Describe("Slack", func() {
	var poster *fakeSlackPoster
	var slackClient notification.Slack

	BeforeEach(func() {
		poster = &fakeSlackPoster{}
		slackClient = notification.NewSlackWithPoster(poster)
	})

	It("sends message successfully", func() {
		err := slackClient.Notify("ch-success", "Hello world")
		Expect(err).To(BeNil())
		Expect(poster.CalledChannel).To(Equal("ch-success"))
	})

	It("returns error when PostMessage fails", func() {
		poster.ReturnError = errors.New("slack error")
		err := slackClient.Notify("ch-fail", "Fail message")
		Expect(err).To(MatchError("failed to send Slack message: slack error"))
	})
})
