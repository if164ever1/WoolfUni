variable "namespace" {
  description = "Kubernetes namespace for Jenkins."
  type        = string
  default     = "jenkins"
}

variable "chart_version" {
  description = "Jenkins Helm chart version."
  type        = string
  default     = "5.9.33"
}

variable "admin_username" {
  description = "Jenkins administrator username."
  type        = string
  default     = "admin"
}

variable "cluster_name" {
  description = "EKS cluster name."
  type        = string
  default     = "final-devops-eks"
}

variable "oidc_provider_arn" {
  description = "EKS IAM OIDC provider ARN for Jenkins agent IRSA."
  type        = string
  default     = ""
}

variable "oidc_provider_url" {
  description = "EKS OIDC provider URL without https://."
  type        = string
  default     = ""
}

variable "ecr_repository_arn" {
  description = "ECR repository ARN Jenkins agents may push to."
  type        = string
  default     = ""
}

variable "ecr_repository_url" {
  description = "ECR repository URL exported to Jenkins pipeline jobs."
  type        = string
  default     = ""
}

variable "aws_region" {
  description = "AWS region exported to Jenkins pipeline jobs."
  type        = string
  default     = "us-west-2"
}

variable "source_repository_url" {
  description = "Source Git repository URL used by the seeded Jenkins pipeline."
  type        = string
  default     = "https://github.com/REPLACE_ME/REPLACE_ME.git"
}

variable "source_project_path" {
  description = "Path from the source repository root to the final project directory."
  type        = string
  default     = "."
}

variable "source_branch" {
  description = "Source Git branch used by the seeded Jenkins pipeline."
  type        = string
  default     = "final-project"
}

variable "jenkinsfile_path" {
  description = "Jenkinsfile path inside the source repository."
  type        = string
  default     = "Django/Jenkinsfile"
}

variable "gitops_repository_url" {
  description = "Git repository URL Jenkins updates after a successful image build."
  type        = string
  default     = "https://github.com/REPLACE_ME/REPLACE_ME.git"
}

variable "gitops_branch" {
  description = "Git branch Jenkins updates with the new image tag."
  type        = string
  default     = "final-project"
}

variable "gitops_values_path" {
  description = "Helm values file Jenkins updates."
  type        = string
  default     = "charts/django-app/values.yaml"
}

variable "github_username" {
  description = "Username stored in the Jenkins GitHub credential."
  type        = string
  default     = "git"
}

variable "github_token" {
  description = "GitHub token stored in Kubernetes and exposed to Jenkins credentials."
  type        = string
  default     = ""
  sensitive   = true
}

variable "tags" {
  description = "Tags applied to IAM resources created for Jenkins."
  type        = map(string)
  default     = {}
}
