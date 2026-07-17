output "vpc_id" {
  description = "ID of the discovered VPC."
  value       = data.aws_vpc.selected.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the discovered VPC."
  value       = data.aws_vpc.selected.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of discovered public subnets."
  value       = data.aws_subnets.public.ids
}

output "private_subnet_ids" {
  description = "IDs of discovered private subnets."
  value       = data.aws_subnets.private.ids
}
