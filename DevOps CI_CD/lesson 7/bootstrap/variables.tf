variable "aws_region" {
  type    = string
  default = "us-west-2"
}

variable "state_bucket_name" {
  description = "Globally unique S3 bucket name. Change this value before apply."
  type        = string
  default     = "if164ever1-lesson-7-terraform-state"
}

variable "lock_table_name" {
  type    = string
  default = "lesson-7-terraform-locks"
}
