variable "namespace" {
  type = string
}

variable "chart_version" {
  type = string
}

variable "service_type" {
  type = string
}

variable "admin_username" {
  type = string
}

variable "github_token" {
  type      = string
  sensitive = true
}

variable "aws_region" {
  type = string
}

variable "ecr_repository_url" {
  type = string
}

variable "ecr_repository_arn" {
  type = string
}

variable "oidc_provider_arn" {
  type = string
}

variable "oidc_provider_url" {
  type = string
}

variable "source_repository_url" {
  type = string
}

variable "source_repository_branch" {
  type = string
}

variable "jenkinsfile_path" {
  type = string
}

variable "gitops_repository_url" {
  type = string
}

variable "gitops_repository_branch" {
  type = string
}

variable "gitops_values_file" {
  type = string
}

variable "agent_service_account_name" {
  type = string
}
