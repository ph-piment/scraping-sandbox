terraform {
  required_version = ">= 1.11.4"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.10.0"
    }
  }
}

provider "aws" {
  region  = "ap-northeast-1"
  profile = "scraping-sandbox"
}

data "aws_caller_identity" "current" {}
