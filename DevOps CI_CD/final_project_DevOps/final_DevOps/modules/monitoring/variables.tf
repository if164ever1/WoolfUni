variable "namespace" {
  description = "Kubernetes namespace for the monitoring stack."
  type        = string
  default     = "monitoring"
}

variable "kube_prometheus_chart_version" {
  description = "kube-prometheus-stack Helm chart version."
  type        = string
  default     = "86.0.1"
}

variable "metrics_server_chart_version" {
  description = "Metrics Server Helm chart version."
  type        = string
  default     = "3.13.1"
}

variable "grafana_admin_username" {
  description = "Grafana administrator username."
  type        = string
  default     = "admin"
}
