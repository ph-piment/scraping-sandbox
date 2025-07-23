package secret_test

import (
	"context"
	"os"

	"scraping-sandbox/internal/infra/secret"
	"scraping-sandbox/test/mocks/clientfakes"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/secretsmanager"
	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
)

var _ = Describe("NotifyBigHoldersSecrets", func() {
	var (
		ctx         = context.Background()
		originalEnv map[string]string
	)

	saveOriginalEnv := func() {
		originalEnv = map[string]string{
			"SLACK_TOKEN":      os.Getenv("SLACK_TOKEN"),
			"SLACK_CHANNEL_ID": os.Getenv("SLACK_CHANNEL_ID"),
			"EDINET_API_KEY":   os.Getenv("EDINET_API_KEY"),
		}
	}

	restoreOriginalEnv := func() {
		for k, v := range originalEnv {
			_ = os.Setenv(k, v)
		}
	}

	setEnv := func(token, channel, api string) {
		_ = os.Setenv("SLACK_TOKEN", token)
		_ = os.Setenv("SLACK_CHANNEL_ID", channel)
		_ = os.Setenv("EDINET_API_KEY", api)
	}

	clearEnv := func() {
		_ = os.Unsetenv("SLACK_TOKEN")
		_ = os.Unsetenv("SLACK_CHANNEL_ID")
		_ = os.Unsetenv("EDINET_API_KEY")
	}

	BeforeEach(saveOriginalEnv)
	AfterEach(restoreOriginalEnv)

	Describe("ExportLoadNotifyBigHoldersFromEnv", func() {
		Context("when all required env vars are set", func() {
			It("returns secrets from environment", func() {
				setEnv("x-slack", "channel-123", "edinet-456")

				secrets := secret.ExportLoadNotifyBigHoldersFromEnv()
				Expect(secrets).ToNot(BeNil())
				Expect(secrets.SlackToken).To(Equal("x-slack"))
				Expect(secrets.SlackChannelID).To(Equal("channel-123"))
				Expect(secrets.EdinetApiKey).To(Equal("edinet-456"))
			})
		})

		Context("when some env vars are missing", func() {
			It("returns nil", func() {
				clearEnv()
				setEnv("", "channel-123", "edinet-456")

				secrets := secret.ExportLoadNotifyBigHoldersFromEnv()
				Expect(secrets).To(BeNil())
			})
		})
	})

	Describe("ExportLoadNotifyBigHoldersFromSecretsManager", func() {
		It("returns secrets parsed from mocked SecretsManager", func() {
			fake := &clientfakes.FakeSecretsManagerClient{}
			fake.GetSecretValueReturns(&secretsmanager.GetSecretValueOutput{
				SecretString: aws.String(`{
				"SLACK_TOKEN": "mock-token",
				"SLACK_CHANNEL_ID": "mock-channel",
				"EDINET_API_KEY": "mock-key"
			}`),
			}, nil)

			secrets, err := secret.ExportLoadNotifyBigHoldersFromSecretsManager(ctx, fake, "any-secret")
			Expect(err).To(BeNil())
			Expect(secrets).ToNot(BeNil())
			Expect(secrets.SlackToken).To(Equal("mock-token"))
		})
	})

	Describe("LoadNotifyBigHolders", func() {
		Context("when env vars are present", func() {
			It("returns env values without calling SecretsManager", func() {
				setEnv("token-env", "channel-env", "api-env")

				fake := &clientfakes.FakeSecretsManagerClient{}

				secrets, err := secret.LoadNotifyBigHolders(ctx, fake)
				Expect(err).To(BeNil())
				Expect(secrets).ToNot(BeNil())
				Expect(secrets.SlackToken).To(Equal("token-env"))
				Expect(secrets.SlackChannelID).To(Equal("channel-env"))
				Expect(secrets.EdinetApiKey).To(Equal("api-env"))
			})
		})

		Context("when env vars are missing", func() {
			It("falls back to mocked SecretsManager and sets env", func() {
				clearEnv()

				fake := &clientfakes.FakeSecretsManagerClient{}
				fake.GetSecretValueReturns(&secretsmanager.GetSecretValueOutput{
					SecretString: aws.String(`{
				"SLACK_TOKEN": "fallback-token",
				"SLACK_CHANNEL_ID": "fallback-channel",
				"EDINET_API_KEY": "fallback-api"
			}`),
				}, nil)

				secrets, err := secret.LoadNotifyBigHolders(ctx, fake)
				Expect(err).To(BeNil())
				Expect(secrets).ToNot(BeNil())
				Expect(os.Getenv("SLACK_TOKEN")).To(Equal("fallback-token"))
				Expect(os.Getenv("SLACK_CHANNEL_ID")).To(Equal("fallback-channel"))
				Expect(os.Getenv("EDINET_API_KEY")).To(Equal("fallback-api"))
			})
		})
	})
})
