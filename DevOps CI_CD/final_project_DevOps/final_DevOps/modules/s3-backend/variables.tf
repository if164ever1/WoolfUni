variable "bucket_name" {
  description = "Globally unique S3 bucket name for Terraform state."
  type        = string
  default     = "replace-with-globally-unique-final-devops-state-bucket"
}

variable "table_name" {
  description = "DynamoDB table name for Terraform state locking."
  type        = string
  default     = "terraform-locks"
}

variable "force_destroy" {
  description = "Allow deleting all objects when the state bucket is intentionally destroyed."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags applied to backend resources."
  type        = map(string)
  default     = {}
}
