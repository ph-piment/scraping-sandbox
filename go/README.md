# notify-big-holders (AWS Lambda in Go)

[![codecov](https://codecov.io/gh/ph-piment/scraping-sandbox/graph/badge.svg?token=ejJtwle3T4)](https://codecov.io/gh/ph-piment/scraping-sandbox)
[![Go](https://img.shields.io/badge/go-1.25%2B-blue.svg)](https://go.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This Go-based AWS Lambda function fetches and analyzes large shareholding disclosures from EDINET (Electronic Disclosure for Investors) and posts updates to a Slack webhook.

## Features

- Written in pure Go, compiled for AWS Lambda (Amazon Linux 2023)
- Loads credentials (e.g., Slack webhook, EDINET token) from AWS Secrets Manager
- Reads and processes company info from `EdinetcodeDlInfo.csv`
- Designed for scheduled execution (e.g., via EventBridge)

## File Structure

```bash
├── cmd/
│   └── lambda/
│       └── notify_big_holders/       # Entry point for AWS Lambda function
│           └── main.go
├── docker/
│   └── app/                          # Docker-related files
│       └── Dockerfile
├── docker-compose.yml               # For local container orchestration
├── go.mod / go.sum                  # Go module dependencies
├── Makefile                         # Build and test automation
├── internal/
│   ├── adapter/
│   │   └── repository/              # Interfaces to external systems (e.g. EDINET)
│   ├── data/                        # Static CSV or auxiliary data (e.g. EdinetcodeDlInfo.csv)
│   ├── domain/                      # Core business logic and domain models
│   ├── infra/
│   │   ├── client/                  # External client implementations (e.g. EDINET API, Secrets Manager)
│   │   ├── notification/           # Slack integration and notification logic
│   │   └── secret/                 # Secret loading logic (env, Secrets Manager)
│   ├── usecase/                     # Application use cases / orchestrators
│   └── utils/                       # Small utility functions (e.g. string helpers)
├── test/
│   └── mocks/
│       ├── clientfakes/            # Generated mocks for external clients
│       ├── notificationfakes/      # Generated mocks for Slack notifier
│       └── repositoryfakes/        # Generated mocks for repository interfaces
└── README.md                        # You're reading this
```

## Build Instructions

You can build this for AWS Lambda using the following Make target:

```bash
make build-notify-big-holders
```

This will:
1. Compile the Go binary for linux/amd64 with GOOS=linux and CGO_ENABLED=0
2. Rename the binary to bootstrap (required by Lambda)
3. Zip it together with the required EdinetcodeDlInfo.csv file
4. Output a deployment package as lambda.zip (in infra/notify_big_holders)

## Secrets
This function expects credentials to be stored in AWS Secrets Manager under the following structure:

### Secret Name
scraping-sandbox-credentials

### Secret Value (JSON)

```json
{
  "EDINET_API_KEY": "hoge",
  "SLACK_TOKEN": "fuga",
  "SLACK_CHANNEL_ID": "#sample"
}
```

## Runtime
AWS Lambda Runtime: provided.al2023

Entrypoint: bootstrap (Go binary)

## Logs
All logs are emitted to CloudWatch Logs via standard output.

## License
MIT License
