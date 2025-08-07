package secret

import (
	"context"

	"scraping-sandbox/internal/infra/client"
)

func ExportLoadNotifyBigHoldersFromEnv() *NotifyBigHoldersSecrets {
	return loadNotifyBigHoldersFromEnv()
}

func ExportLoadNotifyBigHoldersFromSecretsManager(ctx context.Context, client client.SecretsManagerClient, secretName string) (*NotifyBigHoldersSecrets, error) {
	return loadNotifyBigHoldersFromSecretsManager(ctx, client, secretName)
}
