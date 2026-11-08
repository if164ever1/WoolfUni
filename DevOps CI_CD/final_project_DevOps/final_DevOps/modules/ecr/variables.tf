variable "repository_name" {
  description = "ECR repository name."
  type        = string
  default     = "final-devops-django"
}

variable "image_tag_mutability" {
  description = "ECR image tag mutability setting."
  type        = string
  default     = "IMMUTABLE"
}

variable "scan_on_push" {
  description = "Scan container images when they are pushed."
  type        = bool
  default     = true
}

variable "force_delete" {
  description = "Delete images automatically when the ECR repository is destroyed."
  type        = bool
  default     = true
}

variable "image_retention_count" {
  description = "Number of recent tagged images retained."
  type        = number
  default     = 30
}

variable "tags" {
  description = "Tags applied to ECR resources."
  type        = map(string)
  default     = {}
}
