# S3 Frontend outputs
output "frontend_bucket_name" {
  description = "Name of the S3 bucket for frontend hosting"
  value       = aws_s3_bucket.frontend.bucket
}

output "frontend_website_url" {
  description = "Website URL of the S3 bucket"
  value       = "http://${aws_s3_bucket.frontend.bucket}.s3-website-${aws_s3_bucket.frontend.region}.amazonaws.com"
}

# DynamoDB outputs
output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.main.name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.main.arn
} 