variable "namespace" {
  type = string
}

variable "chart_version" {
  type = string
}

variable "service_type" {
  type = string
}

variable "github_token" {
  type      = string
  sensitive = true
}

variable "gitops_repository_url" {
  type = string
}

variable "gitops_repository_branch" {
  type = string
}

variable "application_namespace" {
  type = string
}

variable "application_name" {
  type = string
}

variable "chart_path" {
  type = string
}
