output "namespace" {
  description = "Kubernetes namespace containing Prometheus and Grafana."
  value       = kubernetes_namespace_v1.this.metadata[0].name
}

output "grafana_admin_username" {
  description = "Grafana administrator username."
  value       = var.grafana_admin_username
}

output "grafana_admin_password" {
  description = "Generated Grafana administrator password."
  value       = random_password.grafana.result
  sensitive   = true
}

output "grafana_port_forward_command" {
  description = "Command used to access Grafana locally."
  value       = "kubectl port-forward svc/grafana 3000:80 -n ${var.namespace}"
}

output "prometheus_port_forward_command" {
  description = "Command used to access Prometheus locally."
  value       = "kubectl port-forward svc/prometheus-operated 9090:9090 -n ${var.namespace}"
}
