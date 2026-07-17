variable "release_name" {
  description = "Helm release name used for Argo CD."
  type        = string
  default     = "argo-cd"
}

variable "namespace" {
  description = "Kubernetes namespace used for Argo CD."
  type        = string
  default     = "argocd"
}

variable "chart_version" {
  description = "Optional Argo CD Helm chart version. Empty string uses the repository default."
  type        = string
  default     = ""
}

variable "install_application_chart" {
  description = "Whether to install the local Helm chart containing declarative Argo CD Applications and repositories."
  type        = bool
  default     = false
}
