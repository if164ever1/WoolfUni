variable "vpc_name" {
  description = "Name tag of the existing lesson 5 VPC."
  type        = string
}

variable "cluster_name" {
  description = "EKS cluster name used for Kubernetes subnet tags."
  type        = string
}
