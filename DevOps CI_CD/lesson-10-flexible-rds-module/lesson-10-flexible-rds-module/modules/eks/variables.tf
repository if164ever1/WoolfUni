variable "cluster_name" {
  description = "Name of the EKS cluster."
  type        = string
  default     = "lesson-10-eks"
}

variable "private_subnet_ids" {
  description = "Private subnet IDs used by the EKS cluster and node group."
  type        = list(string)
  default     = []
}

variable "instance_types" {
  description = "EC2 instance types used by the EKS managed node group."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "desired_size" {
  description = "Desired worker-node count."
  type        = number
  default     = 2
}

variable "min_size" {
  description = "Minimum worker-node count."
  type        = number
  default     = 1
}

variable "max_size" {
  description = "Maximum worker-node count."
  type        = number
  default     = 3
}
