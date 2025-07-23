package secret

import (
	"context"
	"encoding/json"
	"fmt"
	"os"

	"scraping-sandbox/internal/infra/client"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/secretsmanager"
)

const (
	secretName = "scraping-sandbox-credentials"
)

type NotifyBigHoldersSecrets struct {
	SlackToken     string `json:"SLACK_TOKEN"`
	SlackChannelID string `json:"SLACK_CHANNEL_ID"`
	EdinetApiKey   string `json:"EDINET_API_KEY"`
}

func LoadNotifyBigHolders(ctx context.Context, client client.SecretsManagerClient) (*NotifyBigHoldersSecrets, error) {
	secrets := loadNotifyBigHoldersFromEnv()
	if secrets != nil {
		return secrets, nil
	}

	secrets, err := loadNotifyBigHoldersFromSecretsManager(ctx, client, secretName)
	if err != nil {
		return nil, err
	}

	if err := os.Setenv("SLACK_TOKEN", secrets.SlackToken); err != nil {
		return nil, fmt.Errorf("failed to set SLACK_TOKEN:: %w", err)
	}
	if err := os.Setenv("SLACK_CHANNEL_ID", secrets.SlackChannelID); err != nil {
		return nil, fmt.Errorf("failed to set SLACK_CHANNEL_ID:: %w", err)
	}
	if err := os.Setenv("EDINET_API_KEY", secrets.EdinetApiKey); err != nil {
		return nil, fmt.Errorf("failed to set EDINET_API_KEY:: %w", err)
	}

	return secrets, nil
}

func loadNotifyBigHoldersFromEnv() *NotifyBigHoldersSecrets {
	slackToken := os.Getenv("SLACK_TOKEN")
	slackChannelID := os.Getenv("SLACK_CHANNEL_ID")
	edinetApiKey := os.Getenv("EDINET_API_KEY")

	if slackToken != "" && slackChannelID != "" && edinetApiKey != "" {
		return &NotifyBigHoldersSecrets{
			SlackToken:     slackToken,
			SlackChannelID: slackChannelID,
			EdinetApiKey:   edinetApiKey,
		}
	}
	return nil
}

func loadNotifyBigHoldersFromSecretsManager(ctx context.Context, client client.SecretsManagerClient, secretName string) (*NotifyBigHoldersSecrets, error) {
	resp, err := client.GetSecretValue(ctx, &secretsmanager.GetSecretValueInput{
		SecretId: aws.String(secretName),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to fetch secret %s: %w", secretName, err)
	}

	var secrets NotifyBigHoldersSecrets
	if err := json.Unmarshal([]byte(*resp.SecretString), &secrets); err != nil {
		return nil, fmt.Errorf("failed to decode secret JSON: %w", err)
	}
	return &secrets, nil
}
