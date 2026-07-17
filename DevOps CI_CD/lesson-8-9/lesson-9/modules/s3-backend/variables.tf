variable "bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name."
}

variable "table_name" {
  type        = string
  description = "DynamoDB lock table name."
}
