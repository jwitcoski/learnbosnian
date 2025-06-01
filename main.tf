terraform {
  required_version = ">= 1.0"
  
  # Add backend configuration for state storage
  backend "s3" {
    bucket = "your-terraform-state-bucket"
    key    = "learnbosnian/terraform.tfstate"
    region = "us-east-1"
  }
  
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