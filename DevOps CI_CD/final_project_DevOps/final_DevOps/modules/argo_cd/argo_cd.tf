resource "random_password" "django_secret_key" {
  length           = 50
  special          = true
  override_special = "!#$%&*+-=?_"
}

resource "kubernetes_namespace_v1" "argocd" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_namespace_v1" "application" {
  metadata {
    name = var.application_namespace
  }
}

resource "kubernetes_secret_v1" "database" {
  metadata {
    name      = "django-app-database"
    namespace = kubernetes_namespace_v1.application.metadata[0].name
  }

  data = {
    DATABASE_PASSWORD  = coalesce(var.database_password, "AWS_MANAGED_PASSWORD_NOT_EXPOSED")
    DJANGO_SECRET_KEY  = random_password.django_secret_key.result
  }

  type = "Opaque"
}

resource "helm_release" "argocd" {
  name       = "argocd"
  namespace  = kubernetes_namespace_v1.argocd.metadata[0].name
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = var.chart_version

  timeout         = 900
  wait            = true
  cleanup_on_fail = true

  values = [file("${path.module}/values.yaml")]
}

resource "helm_release" "applications" {
  name      = "final-project-apps"
  namespace = kubernetes_namespace_v1.argocd.metadata[0].name
  chart     = "${path.module}/charts"

  wait = true

  values = [
    yamlencode({
      applications = [
        {
          name                 = "django-app"
          repoURL              = var.repository_url
          targetRevision       = var.repository_branch
          path                 = var.application_chart_path
          destinationNamespace = var.application_namespace
          helm = {
            parameters = [
              {
                name  = "image.repository"
                value = var.ecr_repository_url
              },
              {
                name  = "config.DATABASE_ENGINE"
                value = var.database_engine == "mysql" ? "mysql" : "postgresql"
              },
              {
                name  = "config.DATABASE_HOST"
                value = var.database_host
              },
              {
                name  = "config.DATABASE_PORT"
                value = tostring(var.database_port)
              },
              {
                name  = "config.DATABASE_NAME"
                value = var.database_name
              },
              {
                name  = "config.DATABASE_USER"
                value = var.database_username
              },
              {
                name  = "existingDatabaseSecret"
                value = kubernetes_secret_v1.database.metadata[0].name
              }
            ]
          }
        }
      ]
      repositories = var.repository_password != "" ? [
        {
          name     = "gitops-repository"
          url      = var.repository_url
          username = var.repository_username
          password = var.repository_password
        }
      ] : []
    })
  ]

  depends_on = [helm_release.argocd, kubernetes_secret_v1.database]
}
