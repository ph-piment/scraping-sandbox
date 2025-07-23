# Infrastructure: notify-big-holders (Terraform + AWS Lambda)

This directory contains Terraform code for deploying the **notify-big-holders** AWS Lambda function, which is written in Go and described [here](../../cmd/lambda/notify_big_holders).

## Overview

The infrastructure provisions:

- An IAM role for Lambda execution with access to:
  - CloudWatch Logs
  - AWS Secrets Manager
- A Lambda function (`notify-big-holders`) running on the `provided.al2023` runtime
- An EventBridge rule that triggers the Lambda at 19:00 JST on weekdays
- Lambda permissions for EventBridge to invoke it
- Secrets Manager integration to provide the function with credentials

## File Structure

```bash
infra/
  └── notify_big_holders/
    ├── main.tf # Provider config and AWS profile
    ├── edinet_notify.tf # Lambda, IAM role, policies
    ├── eventbridge.tf # CloudWatch Events (EventBridge) setup
    └── lambda.zip # Deployment package (Go binary + CSV)
```

## Prerequisites

- AWS CLI profile named `scraping-sandbox` configured in `~/.aws/credentials`
- Terraform CLI installed
- Valid EDINET API token and Slack webhook URL stored in:

### Secret: `scraping-sandbox-credentials`

```json
{
  "EDINET_API_KEY": "hoge",
  "SLACK_TOKEN": "fuga",
  "SLACK_CHANNEL_ID": "#sample"
}
```

# Deployment
Run the following commands to deploy the infrastructure:
cd infra/notify_big_holders

```bash
# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply the changes
terraform apply
```

The Lambda function will be scheduled to run automatically at 19:00 JST on weekdays.
You can also invoke it manually from the AWS Console for testing.

# Related Lambda Code
The actual business logic is written in Go and located at:
📂 cmd/lambda/notify_big_holders

See the Go Lambda README for details on the runtime, build, and behavior.

# License
MIT License
