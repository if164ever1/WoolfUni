output "vpc_id" {
  value = data.aws_vpc.selected.id
}

output "public_subnet_ids" {
  value = data.aws_subnets.public.ids

  precondition {
    condition     = length(data.aws_subnets.public.ids) >= 2
    error_message = "At least two public subnets named ${var.vpc_name}-public-* are required."
  }
}

output "private_subnet_ids" {
  value = data.aws_subnets.private.ids

  precondition {
    condition     = length(data.aws_subnets.private.ids) >= 2
    error_message = "At least two private subnets named ${var.vpc_name}-private-* are required."
  }
}
