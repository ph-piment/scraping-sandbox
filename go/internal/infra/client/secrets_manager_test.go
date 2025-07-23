package client_test

import (
	"context"

	"scraping-sandbox/internal/infra/client"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
)

var _ = Describe("NewSecretsManagerClient", func() {
	var originalLoader func(ctx context.Context, optFns ...func(*config.LoadOptions) error) (aws.Config, error)

	BeforeEach(func() {
		originalLoader = client.LoadAWSConfig
		client.LoadAWSConfig = func(ctx context.Context, optFns ...func(*config.LoadOptions) error) (aws.Config, error) {
			return aws.Config{}, nil
		}
	})

	AfterEach(func() {
		client.LoadAWSConfig = originalLoader
	})

	It("should return a secrets manager client without error", func() {
		sm, err := client.NewSecretsManagerClient(context.Background())
		Expect(err).To(BeNil())
		Expect(sm).ToNot(BeNil())
	})
})
