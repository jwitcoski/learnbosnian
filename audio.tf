variable "recording_password" {
  description = "Shared password for the private voice recording site"
  type        = string
  sensitive   = true
  default     = "GornjiVakuf"
}

variable "audio_token_secret" {
  description = "HMAC secret for recorder session tokens"
  type        = string
  sensitive   = true
  default     = "GornjiVakuf-audio-token"
}

locals {
  audio_bucket_name    = "learn-bosnian-audio-${var.stage}"
  recorder_bucket_name = "learn-bosnian-recorder-${var.stage}"
}

# ---------------------------------------------------------------------------
# Public audio assets (played by the lesson site)
# ---------------------------------------------------------------------------

resource "aws_s3_bucket" "audio" {
  bucket = local.audio_bucket_name

  tags = {
    Environment = var.stage
    Service     = "learnbosnian"
    Purpose     = "voice-over-audio"
  }
}

resource "aws_s3_bucket_public_access_block" "audio" {
  bucket = aws_s3_bucket.audio.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_cors_configuration" "audio" {
  bucket = aws_s3_bucket.audio.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag", "Content-Type"]
    max_age_seconds = 3000
  }
}

resource "aws_cloudfront_origin_access_control" "audio" {
  name                              = "learnbosnian-audio-oac-${var.stage}"
  description                       = "OAC for Learn Bosnian audio clips"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "audio" {
  enabled         = true
  is_ipv6_enabled = true
  comment         = "Learn Bosnian audio clips (${var.stage})"
  price_class     = "PriceClass_100"

  origin {
    domain_name              = aws_s3_bucket.audio.bucket_regional_domain_name
    origin_id                = "s3-audio"
    origin_access_control_id = aws_cloudfront_origin_access_control.audio.id
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "s3-audio"

    viewer_protocol_policy = "redirect-to-https"
    compress               = true

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Environment = var.stage
    Service     = "learnbosnian"
  }
}

resource "aws_s3_bucket_policy" "audio" {
  bucket = aws_s3_bucket.audio.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontServicePrincipalRead"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.audio.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.audio.arn
          }
        }
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.audio]
}

# ---------------------------------------------------------------------------
# Private recorder SPA hosting
# ---------------------------------------------------------------------------

resource "aws_s3_bucket" "recorder" {
  bucket = local.recorder_bucket_name

  tags = {
    Environment = var.stage
    Service     = "learnbosnian"
    Purpose     = "voice-recorder-spa"
  }
}

resource "aws_s3_bucket_public_access_block" "recorder" {
  bucket = aws_s3_bucket.recorder.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_cloudfront_origin_access_control" "recorder" {
  name                              = "learnbosnian-recorder-oac-${var.stage}"
  description                       = "OAC for Learn Bosnian recorder site"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "recorder" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Learn Bosnian voice recorder (${var.stage})"
  default_root_object = "index.html"
  price_class         = "PriceClass_100"

  origin {
    domain_name              = aws_s3_bucket.recorder.bucket_regional_domain_name
    origin_id                = "s3-recorder"
    origin_access_control_id = aws_cloudfront_origin_access_control.recorder.id
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "s3-recorder"

    viewer_protocol_policy = "redirect-to-https"
    compress               = true

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  custom_error_response {
    error_code            = 403
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 0
  }

  custom_error_response {
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 0
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Environment = var.stage
    Service     = "learnbosnian"
  }
}

resource "aws_s3_bucket_policy" "recorder" {
  bucket = aws_s3_bucket.recorder.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontServicePrincipalRead"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.recorder.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.recorder.arn
          }
        }
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.recorder]
}

# ---------------------------------------------------------------------------
# Audio API (login, clip list, presigned upload)
# ---------------------------------------------------------------------------

data "archive_file" "audio_api" {
  type        = "zip"
  source_dir  = "${path.module}/backend"
  output_path = "${path.module}/.terraform/audio-api.zip"
  excludes = [
    ".serverless"
  ]
}

resource "aws_iam_role" "audio_api" {
  name = "learnbosnian-audio-api-${var.stage}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "audio_api" {
  name = "learnbosnian-audio-api-${var.stage}"
  role = aws_iam_role.audio_api.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:Query",
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ]
        Resource = [
          aws_dynamodb_table.main.arn,
          "${aws_dynamodb_table.main.arn}/index/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:HeadObject"
        ]
        Resource = "${aws_s3_bucket.audio.arn}/*"
      }
    ]
  })
}

resource "aws_lambda_function" "audio_api" {
  function_name    = "learnbosnian-audio-api-${var.stage}"
  role             = aws_iam_role.audio_api.arn
  handler          = "handlers/audioApi.handler"
  runtime          = "nodejs18.x"
  filename         = data.archive_file.audio_api.output_path
  source_code_hash = data.archive_file.audio_api.output_base64sha256
  timeout          = 15
  memory_size      = 256

  environment {
    variables = {
      STAGE               = var.stage
      DYNAMODB_TABLE      = aws_dynamodb_table.main.name
      AUDIO_BUCKET        = aws_s3_bucket.audio.bucket
      RECORDING_PASSWORD  = var.recording_password
      AUDIO_TOKEN_SECRET  = var.audio_token_secret
      AUDIO_PUBLIC_BASE   = "https://${aws_cloudfront_distribution.audio.domain_name}"
    }
  }

  tags = {
    Environment = var.stage
    Service     = "learnbosnian"
  }
}

resource "aws_apigatewayv2_api" "audio" {
  name          = "learnbosnian-audio-${var.stage}"
  protocol_type = "HTTP"

  cors_configuration {
    allow_headers = ["content-type", "authorization"]
    allow_methods = ["GET", "POST", "OPTIONS"]
    allow_origins = ["*"]
    max_age       = 300
  }
}

resource "aws_apigatewayv2_integration" "audio" {
  api_id                 = aws_apigatewayv2_api.audio.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.audio_api.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "audio_proxy" {
  api_id    = aws_apigatewayv2_api.audio.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.audio.id}"
}

resource "aws_apigatewayv2_route" "audio_root" {
  api_id    = aws_apigatewayv2_api.audio.id
  route_key = "ANY /"
  target    = "integrations/${aws_apigatewayv2_integration.audio.id}"
}

resource "aws_apigatewayv2_stage" "audio" {
  api_id      = aws_apigatewayv2_api.audio.id
  name        = var.stage
  auto_deploy = true
}

resource "aws_lambda_permission" "audio_api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.audio_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.audio.execution_arn}/*/*"
}
