.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  lint                     # Run tflint on all terraform directories"
	@echo "  deploy-notify-big-holders  # Build Go Lambda and apply Terraform"

TFLINT_DIRS := $(shell find . -type f -name "*.tf" -exec dirname {} \; | sort -u)

.PHONY: lint
lint:
	@for dir in $(TFLINT_DIRS); do \
		echo "🔍 Running tflint in $$dir"; \
		tflint --chdir=$$dir || exit 1; \
	done

.PHONY: deploy-notify-big-holders
deploy-notify-big-holders:
	cd ../go && make build-notify-big-holders
	cd notify_big_holders && terraform apply -auto-approve
