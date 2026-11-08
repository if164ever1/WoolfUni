variable "aws_region" {
  description = "AWS region used by the existing VPC and new resources."
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "Base project name."
  type        = string
  default     = "lesson-7"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}

variable "existing_vpc_name" {
  description = "Name tag of the VPC created in lesson 5."
  type        = string
  default     = "lesson-5-vpc"
}

variable "cluster_name" {
  description = "EKS cluster name."
  type        = string
  default     = "lesson-7-eks"
}

variable "ecr_repository_name" {
  description = "ECR repository name."
  type        = string
  default     = "lesson-7-django"
}

variable "node_instance_types" {
  description = "EC2 instance types for the managed node group."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "node_desired_size" {
  type    = number
  default = 2
}

variable "node_min_size" {
  type    = number
  default = 2
}

variable "node_max_size" {
  type    = number
  default = 4
}
