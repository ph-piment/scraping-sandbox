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
