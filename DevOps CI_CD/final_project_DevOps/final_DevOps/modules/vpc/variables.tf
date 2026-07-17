variable "name" {
  description = "Name prefix for VPC resources."
  type        = string
  default     = "final-devops-dev"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.40.0.0/16"
}

variable "availability_zone_count" {
  description = "Number of availability zones to use."
  type        = number
  default     = 3
}

variable "enable_nat_gateway" {
  description = "Create NAT Gateway resources for private subnet internet egress."
  type        = bool
  default     = true
}

variable "single_nat_gateway" {
  description = "Use one shared NAT Gateway instead of one per availability zone."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags applied to VPC resources."
  type        = map(string)
  default     = {}
}
