package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"scraping-sandbox/internal/adapter/repository"
	"scraping-sandbox/internal/infra/client"
	"scraping-sandbox/internal/infra/notification"
	"scraping-sandbox/internal/infra/secret"
	"scraping-sandbox/internal/usecase"

	"github.com/aws/aws-lambda-go/lambda"
)

type Event struct {
	Date string `json:"date"`
}

func Handler(ctx context.Context, e Event) (string, error) {
	date := e.Date
	if date == "" {
		date = time.Now().AddDate(0, 0, -1).Format("2006-01-02")
	}

	client, err := client.NewSecretsManagerClient(ctx)
	if err != nil {
		return "", fmt.Errorf("failed to create secrets manager client: %w", err)
	}

	secrets, err := secret.LoadNotifyBigHolders(ctx, client)
	if err != nil {
		return "", fmt.Errorf("failed to load secrets: %w", err)
	}

	if err = usecase.NewEdinetUsecase(
		repository.NewEdinetRepository(secrets.EdinetApiKey),
		notification.NewSlack(secrets.SlackToken),
	).NotifyBigHolders(ctx, date, secrets.SlackChannelID); err != nil {
		return "", fmt.Errorf("failed to notify big holders: %w", err)
	}

	return fmt.Sprintf("Notification sent for date: %s", date), nil
}

func main() {
	if os.Getenv("AWS_LAMBDA_FUNCTION_NAME") != "" {
		lambda.Start(Handler)
		return
	}

	ctx := context.Background()
	res, err := Handler(ctx, Event{
		Date: time.Now().AddDate(0, 0, -1).Format("2006-01-02"),
	})
	if err != nil {
		log.Fatalf("failed to run locally: %v", err)
	}
	fmt.Println(res)
}
