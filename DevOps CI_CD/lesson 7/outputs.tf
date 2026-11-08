output "vpc_id" {
  description = "Existing lesson 5 VPC ID."
  value       = module.vpc.vpc_id
}

output "private_subnet_ids" {
  description = "Private subnets used by EKS."
  value       = module.vpc.private_subnet_ids
}

output "public_subnet_ids" {
  description = "Public subnets used by public load balancers."
  value       = module.vpc.public_subnet_ids
}

output "cluster_name" {
  value = module.eks.cluster_name
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "ecr_repository_url" {
  value = module.ecr.repository_url
}

output "kubectl_config_command" {
  value = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}"
}

output "aws_region" {
  value = var.aws_region
}
