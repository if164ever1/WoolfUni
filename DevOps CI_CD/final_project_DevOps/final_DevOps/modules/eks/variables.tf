variable "cluster_name" {
  description = "EKS cluster name."
  type        = string
  default     = "final-devops-eks"
}

variable "kubernetes_version" {
  description = "Kubernetes version for EKS."
  type        = string
  default     = "1.36"
}

variable "vpc_id" {
  description = "VPC ID where EKS is deployed."
  type        = string
  default     = ""
}

variable "private_subnet_ids" {
  description = "Private subnet IDs used by EKS control-plane ENIs and worker nodes."
  type        = list(string)
  default     = []
}

variable "public_access_cidrs" {
  description = "CIDRs allowed to access the public Kubernetes API endpoint."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "node_instance_types" {
  description = "EC2 instance types used by the managed node group."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "node_capacity_type" {
  description = "Managed node group capacity type."
  type        = string
  default     = "ON_DEMAND"
}

variable "node_desired_size" {
  description = "Desired managed node group size."
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "Minimum managed node group size."
  type        = number
  default     = 2
}

variable "node_max_size" {
  description = "Maximum managed node group size."
  type        = number
  default     = 4
}

variable "node_disk_size" {
  description = "EBS root volume size for EKS worker nodes."
  type        = number
  default     = 30
}

variable "cluster_log_retention_days" {
  description = "CloudWatch retention period for EKS control-plane logs."
  type        = number
  default     = 7
}

variable "enabled_cluster_log_types" {
  description = "EKS control-plane log types sent to CloudWatch."
  type        = list(string)
  default     = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
}

variable "tags" {
  description = "Tags applied to EKS resources."
  type        = map(string)
  default     = {}
}
