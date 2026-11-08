output "internal_url" {
  value = "http://jenkins.${var.namespace}.svc.cluster.local:8080"
}

output "port_forward_command" {
  value = "kubectl port-forward service/jenkins 8080:8080 --namespace ${var.namespace}"
}

output "admin_password" {
  value     = random_password.admin.result
  sensitive = true
}

output "agent_role_arn" {
  value = aws_iam_role.agent.arn
}
