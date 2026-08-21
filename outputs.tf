output "frontend_bucket_name" {
  description = "Name of the S3 bucket for frontend hosting"
  value       = aws_s3_bucket.frontend.bucket
}

output "cloudfront_domain_name" {
  description = "CloudFront distribution domain name"
  value       = aws_cloudfront_distribution.frontend.domain_name
}

output "cloudfront_url" {
  description = "CloudFront domain URL (still valid; prefer site_url)"
  value       = "https://${aws_cloudfront_distribution.frontend.domain_name}"
}

output "site_url" {
  description = "Public HTTPS URL for the lesson site"
  value       = "https://${var.site_domain}"
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID"
  value       = aws_cloudfront_distribution.frontend.id
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.main.name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.main.arn
}

output "audio_bucket_name" {
  description = "S3 bucket for voice-over clips"
  value       = aws_s3_bucket.audio.bucket
}

output "audio_cloudfront_url" {
  description = "HTTPS base URL for public audio playback"
  value       = "https://${aws_cloudfront_distribution.audio.domain_name}"
}

output "audio_cloudfront_distribution_id" {
  description = "CloudFront distribution ID for audio clips"
  value       = aws_cloudfront_distribution.audio.id
}

output "recorder_bucket_name" {
  description = "S3 bucket for the private recorder SPA"
  value       = aws_s3_bucket.recorder.bucket
}

output "recorder_cloudfront_url" {
  description = "HTTPS URL for the private voice recorder site"
  value       = "https://${aws_cloudfront_distribution.recorder.domain_name}"
}

output "recorder_cloudfront_distribution_id" {
  description = "CloudFront distribution ID for the recorder site"
  value       = aws_cloudfront_distribution.recorder.id
}

output "audio_api_url" {
  description = "HTTP API base URL for recorder login/upload"
  value       = aws_apigatewayv2_stage.audio.invoke_url
}
