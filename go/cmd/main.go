package main

import (
	"context"
	"log"

	"scraping-sandbox/internal/adapter/repository"
	"scraping-sandbox/internal/infra/notification"
	"scraping-sandbox/internal/infra/secret"
	"scraping-sandbox/internal/usecase"
)

func main() {
	ctx := context.Background()

	secrets, err := secret.LoadNotifyBigHolders(ctx)
	if err != nil {
		log.Fatalf("failed to load secrets: %v", err)
	}

	if err := usecase.NewEdinetUsecase(
		repository.NewEdinetRepository(secrets.EdinetApiKey),
		notification.NewSlack(secrets.SlackToken),
	).NotifyBigHolders(ctx, "2025-07-16", secrets.SlackChannelID); err != nil {
		log.Fatalf("failed to notify big holders: %v", err)
	}
}
