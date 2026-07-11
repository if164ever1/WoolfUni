output "internal_url" {
  value = "http://argo-cd-argocd-server.${var.namespace}.svc.cluster.local"
}

output "port_forward_command" {
  value = "kubectl port-forward service/argo-cd-argocd-server 8081:80 --namespace ${var.namespace}"
}

output "admin_password" {
  value     = random_password.admin.result
  sensitive = true
}
