.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  lint        Run linters using golangci-lint"
	@echo "  format      Auto-format using gofumpt and goimports"
	@echo "  test        Run Go tests"
	@echo "  gen-mock    Generate Go mocks using go generate"
	@echo "  lint-test   Run both lint and test"
	@echo "  run-notify-big-holders  Run the notify_big_holders Lambda function locally"
	@echo "  build-notify-big-holders Build the notify_big_holders Lambda function for deployment"
	@echo ""

.PHONY: lint
lint:
	docker-compose run -w /app --rm lint golangci-lint run -c ./.golangci.yml --print-resources-usage -v

.PHONY: format
format:
	docker-compose run -w /app --rm dev gofumpt -l -w .
	docker-compose run -w /app --rm dev goimports -w .

.PHONY: test
test:
	docker-compose run -w /app --rm dev go test ./... -v

.PHONY: gen-mock
gen-mock:
	docker-compose run -w /app --rm dev go generate ./...

.PHONY: lint-test
lint-test:
	make lint
	make test

.PHONY: run-notify-big-holders
run-notify-big-holders:
	LOCAL_EXEC=1 go run cmd/lambda/notify_big_holders/main.go

.PHONY: build-notify-big-holders
build-notify-big-holders:
	GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -o bootstrap cmd/lambda/notify_big_holders/main.go
	zip -r ../infra/notify_big_holders/lambda.zip bootstrap internal/data/EdinetcodeDlInfo.csv
	rm bootstrap
