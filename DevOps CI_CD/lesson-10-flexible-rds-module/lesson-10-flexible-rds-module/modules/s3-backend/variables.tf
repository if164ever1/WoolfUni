variable "bucket_name" {
  description = "Globally unique S3 bucket name for Terraform state."
  type        = string
  default     = "your-name-terraform-state"
}

variable "table_name" {
  description = "DynamoDB table name for Terraform state locking."
  type        = string
  default     = "terraform-locks"
}
