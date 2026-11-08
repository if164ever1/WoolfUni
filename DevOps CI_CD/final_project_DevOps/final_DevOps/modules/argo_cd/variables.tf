variable "namespace" {
  description = "Kubernetes namespace for Argo CD."
  type        = string
  default     = "argocd"
}

variable "chart_version" {
  description = "Argo CD Helm chart version."
  type        = string
  default     = "10.1.3"
}

variable "repository_url" {
  description = "GitOps repository watched by Argo CD."
  type        = string
  default     = "https://github.com/REPLACE_ME/REPLACE_ME.git"
}


variable "repository_username" {
  description = "Optional Git username used by Argo CD for a private GitOps repository."
  type        = string
  default     = ""
}

variable "repository_password" {
  description = "Optional Git token/password used by Argo CD for a private GitOps repository."
  type        = string
  default     = ""
  sensitive   = true
}

variable "repository_branch" {
  description = "Git revision watched by Argo CD."
  type        = string
  default     = "final-project"
}

variable "application_chart_path" {
  description = "Path to the Django Helm chart in the GitOps repository."
  type        = string
  default     = "charts/django-app"
}

variable "application_namespace" {
  description = "Kubernetes namespace where Argo CD deploys Django."
  type        = string
  default     = "django-app"
}

variable "ecr_repository_url" {
  description = "ECR repository URL passed to the Django Helm chart."
  type        = string
  default     = ""
}

variable "database_engine" {
  description = "Django database engine selection."
  type        = string
  default     = "postgres"
}

variable "database_host" {
  description = "Database hostname passed to Django through Helm parameters."
  type        = string
  default     = ""
}

variable "database_port" {
  description = "Database TCP port."
  type        = number
  default     = 5432
}

variable "database_name" {
  description = "Application database name."
  type        = string
  default     = "appdb"
}

variable "database_username" {
  description = "Application database username."
  type        = string
  default     = "dbadmin"
}

variable "database_password" {
  description = "Database password stored as a Kubernetes Secret."
  type        = string
  default     = null
  sensitive   = true
}
