resource "random_password" "admin" {
  length           = 24
  special          = true
  override_special = "!@#%_-"
}

locals {
  argocd_dynamic_values = {
    configs = {
      secret = {
        argocdServerAdminPassword = bcrypt(random_password.admin.result)
      }
    }
    server = {
      service = {
        type = var.service_type
      }
    }
  }
}

resource "helm_release" "argo_cd" {
  name       = "argo-cd"
  namespace  = kubernetes_namespace_v1.this.metadata[0].name
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = var.chart_version

  atomic          = true
  cleanup_on_fail = true
  timeout         = 1200
  wait            = true

  values = [
    file("${path.module}/values.yaml"),
    yamlencode(local.argocd_dynamic_values)
  ]
}

resource "helm_release" "applications" {
  name      = "argocd-applications"
  namespace = kubernetes_namespace_v1.this.metadata[0].name
  chart     = "${path.module}/charts/argocd-apps"

  atomic          = true
  cleanup_on_fail = true
  timeout         = 300
  wait            = true

  values = [
    yamlencode({
      repositories = []
      applications = [
        {
          name             = var.application_name
          namespace        = kubernetes_namespace_v1.this.metadata[0].name
          project          = "default"
          repoURL          = var.gitops_repository_url
          targetRevision   = var.gitops_repository_branch
          path             = var.chart_path
          destinationServer = "https://kubernetes.default.svc"
          destinationNamespace = var.application_namespace
          automated = {
            prune    = true
            selfHeal = true
          }
          syncOptions = [
            "CreateNamespace=true",
            "PruneLast=true",
            "ApplyOutOfSyncOnly=true"
          ]
        }
      ]
    })
  ]

  depends_on = [helm_release.argo_cd, kubernetes_secret_v1.repository]
}
