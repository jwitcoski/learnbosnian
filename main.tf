terraform {
  required_version = ">= 1.0"
  
  # Remove backend configuration for now - will use local state
  # backend "s3" {
  #   bucket = "your-terraform-state-bucket"
  #   key    = "learnbosnian/terraform.tfstate"
  #   region = "us-east-1"
  # }
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

# Add variable declaration
variable "stage" {
  description = "Deployment stage (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "frontend" {
  bucket = "learn-bosnian-frontend-${var.stage}"
}

resource "aws_dynamodb_table" "main" {
  name           = "learnbosnian-table-${var.stage}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "pk"
  range_key      = "sk"
  
  attribute {
    name = "pk"
    type = "S"
  }
  
  attribute {
    name = "sk" 
    type = "S"
  }
  
  attribute {
    name = "gsi1pk"
    type = "S"
  }
  
  attribute {
    name = "gsi1sk"
    type = "S"
  }

  global_secondary_index {
    name     = "GSI1"
    hash_key = "gsi1pk"
    range_key = "gsi1sk"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Environment = var.stage
    Service     = "learnbosnian"
  }
}