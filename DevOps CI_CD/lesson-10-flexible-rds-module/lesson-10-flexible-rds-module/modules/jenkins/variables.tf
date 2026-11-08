variable "release_name" {
  description = "Helm release name used for Jenkins."
  type        = string
  default     = "jenkins"
}

variable "namespace" {
  description = "Kubernetes namespace used for Jenkins."
  type        = string
  default     = "jenkins"
}

variable "chart_version" {
  description = "Optional Jenkins Helm chart version. Empty string uses the repository default."
  type        = string
  default     = ""
}
