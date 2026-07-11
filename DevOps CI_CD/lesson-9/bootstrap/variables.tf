variable "aws_region" {
  type        = string
  description = "AWS region for the backend resources."
  default     = "us-west-2"
}

variable "state_bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name for Terraform state."
}

variable "lock_table_name" {
  type        = string
  description = "DynamoDB table used for Terraform state locking."
  default     = "lesson-8-9-terraform-locks"
}
