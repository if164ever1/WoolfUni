variable "existing_vpc_name" {
  description = "Name tag of the existing VPC."
  type        = string
  default     = "lesson-5-vpc"
}

variable "public_subnet_name_pattern" {
  description = "Name-tag wildcard used to discover public subnets."
  type        = string
  default     = "lesson-5-vpc-public-*"
}

variable "private_subnet_name_pattern" {
  description = "Name-tag wildcard used to discover private subnets."
  type        = string
  default     = "lesson-5-vpc-private-*"
}
