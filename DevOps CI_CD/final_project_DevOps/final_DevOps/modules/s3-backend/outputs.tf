output "bucket_name" {
  description = "Name of the Terraform state S3 bucket."
  value       = aws_s3_bucket.state.bucket
}

output "bucket_arn" {
  description = "ARN of the Terraform state S3 bucket."
  value       = aws_s3_bucket.state.arn
}

output "table_name" {
  description = "Name of the DynamoDB state lock table."
  value       = aws_dynamodb_table.locks.name
}

output "table_arn" {
  description = "ARN of the DynamoDB state lock table."
  value       = aws_dynamodb_table.locks.arn
}
