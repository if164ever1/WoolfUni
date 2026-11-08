variable "cluster_name" {
  type        = string
  description = "EKS cluster name."
}

variable "kubernetes_version" {
  type        = string
  description = "EKS Kubernetes minor version."
}

variable "subnet_ids" {
  type        = list(string)
  description = "Private subnet IDs used by EKS and managed nodes."
}

variable "endpoint_public_access_cidrs" {
  type        = list(string)
  description = "CIDRs allowed to reach the public EKS endpoint."
}

variable "node_instance_types" {
  type        = list(string)
  description = "EC2 instance types for the managed node group."
}

variable "node_desired_size" {
  type = number
}

variable "node_min_size" {
  type = number
}

variable "node_max_size" {
  type = number
}
