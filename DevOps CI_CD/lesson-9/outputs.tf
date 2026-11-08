output "vpc_id" {
  description = "Existing lesson-5 VPC ID."
  value       = module.vpc.vpc_id
}

output "private_subnet_ids" {
  description = "Private subnet IDs used by EKS."
  value       = module.vpc.private_subnet_ids
}

output "cluster_name" {
  value       = module.eks.cluster_name
  description = "Amazon EKS cluster name."
}

output "cluster_endpoint" {
  value       = module.eks.cluster_endpoint
  description = "Amazon EKS API endpoint."
}

output "ecr_repository_url" {
  value       = module.ecr.repository_url
  description = "ECR repository URI used by Kaniko."
}

output "jenkins_internal_url" {
  value       = module.jenkins.internal_url
  description = "Jenkins in-cluster URL."
}

output "jenkins_port_forward_command" {
  value       = module.jenkins.port_forward_command
  description = "Command to access Jenkins when service type is ClusterIP."
}

output "jenkins_admin_username" {
  value = var.jenkins_admin_username
}

output "jenkins_admin_password" {
  value       = module.jenkins.admin_password
  description = "Initial Jenkins administrator password."
  sensitive   = true
}

output "argocd_internal_url" {
  value       = module.argo_cd.internal_url
  description = "Argo CD in-cluster URL."
}

output "argocd_port_forward_command" {
  value       = module.argo_cd.port_forward_command
  description = "Command to access Argo CD when service type is ClusterIP."
}

output "argocd_admin_password" {
  value       = module.argo_cd.admin_password
  description = "Initial Argo CD admin password."
  sensitive   = true
}

output "configure_kubectl_command" {
  description = "PowerShell command that configures kubectl."
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}"
}

output "aws_region" {
  value = var.aws_region
}

output "metrics_server_release" {
  description = "Metrics Server Helm release used by the Django HPA."
  value       = helm_release.metrics_server.name
}
