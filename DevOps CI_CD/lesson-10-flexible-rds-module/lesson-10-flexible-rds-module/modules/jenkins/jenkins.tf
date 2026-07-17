resource "helm_release" "this" {
  name             = var.release_name
  repository       = "https://charts.jenkins.io"
  chart            = "jenkins"
  namespace        = var.namespace
  create_namespace = true
  version          = var.chart_version == "" ? null : var.chart_version

  values = [file("${path.module}/values.yaml")]
}
