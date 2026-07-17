resource "random_password" "grafana" {
  length           = 24
  special          = true
  override_special = "!#$%&*+-=?_"
}

resource "kubernetes_namespace_v1" "this" {
  metadata {
    name = var.namespace
  }
}

resource "helm_release" "metrics_server" {
  name       = "metrics-server"
  namespace  = "kube-system"
  repository = "https://kubernetes-sigs.github.io/metrics-server/"
  chart      = "metrics-server"
  version    = var.metrics_server_chart_version

  timeout         = 600
  wait            = true
  cleanup_on_fail = true

  values = [
    yamlencode({
      replicas = 2
      args = [
        "--kubelet-preferred-address-types=InternalIP,Hostname,ExternalIP"
      ]
      resources = {
        requests = {
          cpu    = "100m"
          memory = "200Mi"
        }
      }
    })
  ]
}

resource "helm_release" "kube_prometheus_stack" {
  name       = "kube-prometheus-stack"
  namespace  = kubernetes_namespace_v1.this.metadata[0].name
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  version    = var.kube_prometheus_chart_version

  timeout         = 1200
  wait            = true
  cleanup_on_fail = true

  values = [
    templatefile("${path.module}/values.yaml", {
      grafana_admin_username = var.grafana_admin_username
      grafana_admin_password = random_password.grafana.result
    })
  ]

  depends_on = [helm_release.metrics_server]
}
