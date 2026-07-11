variable "project_name" {
  description = "Common name prefix for lesson 8-9 resources."
  type        = string
  default     = "lesson-8-9"
}

variable "environment" {
  description = "Environment tag and Kubernetes target environment."
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region used by the existing VPC and all new resources."
  type        = string
  default     = "us-west-2"
}

variable "existing_vpc_name" {
  description = "Name tag of the VPC created by lesson 5."
  type        = string
  default     = "lesson-5-vpc"
}

variable "cluster_name" {
  description = "Amazon EKS cluster name."
  type        = string
  default     = "lesson-8-9-eks"
}

variable "kubernetes_version" {
  description = "Amazon EKS Kubernetes minor version."
  type        = string
  default     = "1.36"
}

variable "node_instance_types" {
  description = "EC2 instance types used by the managed node group."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "node_desired_size" {
  type        = number
  description = "Desired managed node group size."
  default     = 2
}

variable "node_min_size" {
  type        = number
  description = "Minimum managed node group size."
  default     = 2
}

variable "node_max_size" {
  type        = number
  description = "Maximum managed node group size."
  default     = 4
}

variable "cluster_endpoint_public_access_cidrs" {
  description = "CIDRs allowed to access the public EKS API endpoint. Restrict this in real environments."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "ecr_repository_name" {
  description = "ECR repository that stores Django images."
  type        = string
  default     = "lesson-8-9-django"
}


variable "metrics_server_chart_version" {
  description = "Pinned Metrics Server Helm chart version required by HPA."
  type        = string
  default     = "3.13.1"
}

variable "jenkins_chart_version" {
  description = "Pinned official Jenkins Helm chart version."
  type        = string
  default     = "5.9.33"
}

variable "jenkins_namespace" {
  type        = string
  description = "Namespace for Jenkins."
  default     = "jenkins"
}

variable "jenkins_service_type" {
  type        = string
  description = "Jenkins Service type: ClusterIP, NodePort or LoadBalancer."
  default     = "ClusterIP"

  validation {
    condition     = contains(["ClusterIP", "NodePort", "LoadBalancer"], var.jenkins_service_type)
    error_message = "jenkins_service_type must be ClusterIP, NodePort or LoadBalancer."
  }
}

variable "jenkins_admin_username" {
  type        = string
  description = "Initial Jenkins administrator username."
  default     = "admin"
}

variable "source_repository_url" {
  description = "Git repository containing this Jenkinsfile and Django source."
  type        = string
  default     = "https://github.com/if164ever1/WoolfUni.git"
}

variable "source_repository_branch" {
  description = "Branch monitored by the Jenkins pipeline job."
  type        = string
  default     = "lesson-8-9"
}

variable "jenkinsfile_path" {
  description = "Path to Jenkinsfile inside source_repository_url."
  type        = string
  default     = "DevOps CI_CD/lesson-8-9/Jenkinsfile"
}

variable "gitops_repository_url" {
  description = "Separate GitOps repository watched by Argo CD and updated by Jenkins."
  type        = string
  default     = "https://github.com/if164ever1/lesson-8-9-gitops.git"
}

variable "gitops_repository_branch" {
  type        = string
  description = "GitOps branch updated by Jenkins and watched by Argo CD."
  default     = "main"
}

variable "gitops_values_file" {
  type        = string
  description = "Path Jenkins updates inside the GitOps repository."
  default     = "charts/django-app/values.yaml"
}

variable "github_token" {
  description = "GitHub PAT with read access to source repo and read/write Contents access to GitOps repo. Supply through TF_VAR_github_token."
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.github_token) >= 20
    error_message = "github_token must be a real GitHub token supplied securely, not a placeholder."
  }
}

variable "argocd_chart_version" {
  description = "Pinned official Argo CD Helm chart version."
  type        = string
  default     = "10.1.3"
}

variable "argocd_namespace" {
  type        = string
  description = "Namespace for Argo CD."
  default     = "argocd"
}

variable "argocd_service_type" {
  type        = string
  description = "Argo CD server Service type."
  default     = "ClusterIP"

  validation {
    condition     = contains(["ClusterIP", "NodePort", "LoadBalancer"], var.argocd_service_type)
    error_message = "argocd_service_type must be ClusterIP, NodePort or LoadBalancer."
  }
}

variable "application_namespace" {
  type        = string
  description = "Namespace where Argo CD deploys the Django application."
  default     = "django-app"
}
