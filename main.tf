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