package secret

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/secretsmanager"
)

type NotifyBigHoldersSecrets struct {
	SlackToken     string `json:"SLACK_TOKEN"`
	SlackChannelID string `json:"SLACK_CHANNEL_ID"`
	EdinetApiKey   string `json:"EDINET_API_KEY"`
}

func LoadNotifyBigHolders(ctx context.Context) (*NotifyBigHoldersSecrets, error) {
	// Try environment variables first
	slackToken := os.Getenv("SLACK_TOKEN")
	slackChannelID := os.Getenv("SLACK_CHANNEL_ID")
	edinetApiKey := os.Getenv("EDINET_API_KEY")

	if slackToken != "" && slackChannelID != "" && edinetApiKey != "" {
		return &NotifyBigHoldersSecrets{
			SlackToken:     slackToken,
			SlackChannelID: slackChannelID,
			EdinetApiKey:   edinetApiKey,
		}, nil
	}

	// Otherwise, fetch from Secrets Manager
	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to load AWS config: %w", err)
	}

	client := secretsmanager.NewFromConfig(cfg)
	secretName := "notify-big-holders"
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

	// Set to env for consistency across app
	if err := os.Setenv("SLACK_TOKEN", secrets.SlackToken); err != nil {
		log.Printf("failed to set SLACK_TOKEN: %v", err)
	}
	if err := os.Setenv("SLACK_CHANNEL_ID", secrets.SlackChannelID); err != nil {
		log.Printf("failed to set SLACK_CHANNEL_ID: %v", err)
	}
	if err := os.Setenv("EDINET_API_KEY", secrets.EdinetApiKey); err != nil {
		log.Printf("failed to set EDINET_API_KEY: %v", err)
	}

	return &secrets, nil
}
