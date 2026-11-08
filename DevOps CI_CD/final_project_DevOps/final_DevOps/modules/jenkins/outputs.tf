output "namespace" {
  description = "Kubernetes namespace containing Jenkins."
  value       = kubernetes_namespace_v1.this.metadata[0].name
}

output "service_name" {
  description = "Jenkins Kubernetes Service name."
  value       = helm_release.jenkins.name
}

output "admin_username" {
  description = "Jenkins administrator username."
  value       = var.admin_username
}

output "admin_password" {
  description = "Generated Jenkins administrator password."
  value       = random_password.admin.result
  sensitive   = true
}

output "agent_role_arn" {
  description = "IAM role assumed by Jenkins Kubernetes agents through IRSA."
  value       = aws_iam_role.agent.arn
}

output "port_forward_command" {
  description = "Command used to access Jenkins locally."
  value       = "kubectl port-forward svc/jenkins 8080:8080 -n ${var.namespace}"
}
