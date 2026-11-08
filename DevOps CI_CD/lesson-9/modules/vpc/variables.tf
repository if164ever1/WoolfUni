variable "vpc_name" {
  type        = string
  description = "Name tag of the existing lesson-5 VPC."
}

variable "cluster_name" {
  type        = string
  description = "EKS cluster name used for subnet discovery tags."
}
