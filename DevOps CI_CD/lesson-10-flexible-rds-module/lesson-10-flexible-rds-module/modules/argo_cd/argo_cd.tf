resource "helm_release" "this" {
  name             = var.release_name
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  namespace        = var.namespace
  create_namespace = true
  version          = var.chart_version == "" ? null : var.chart_version

  values = [file("${path.module}/values.yaml")]
}

resource "helm_release" "applications" {
  count = var.install_application_chart ? 1 : 0

  name      = "${var.release_name}-applications"
  chart     = "${path.module}/charts"
  namespace = var.namespace

  depends_on = [helm_release.this]
}
