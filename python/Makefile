.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  lint        Run all linters (flake8, black --check, isort --check, mypy, pylint)"
	@echo "  format      Auto-format using black and isort"
	@echo "  test        Run pytest tests"
	@echo "  lint-test   Run both lint and test"
	@echo ""

.PHONY: lint
lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	black . --check
	isort . --check-only
	mypy .
	pylint .

.PHONY: format
format:
	black .
	isort .

.PHONY: test
test:
	pytest .

.PHONY: lint-test
lint-test: lint test
