output "namespace" {
  description = "Kubernetes namespace containing Argo CD."
  value       = kubernetes_namespace_v1.argocd.metadata[0].name
}

output "server_service_name" {
  description = "Argo CD server Kubernetes Service name."
  value       = "argocd-server"
}

output "application_name" {
  description = "Argo CD Application name managed by the local applications chart."
  value       = "django-app"
}

output "port_forward_command" {
  description = "Command used to access the Argo CD UI locally."
  value       = "kubectl port-forward svc/argocd-server 8081:443 -n ${var.namespace}"
}

output "initial_admin_password_command" {
  description = "Command used to read the initial Argo CD administrator password."
  value       = "kubectl -n ${var.namespace} get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 --decode"
}
