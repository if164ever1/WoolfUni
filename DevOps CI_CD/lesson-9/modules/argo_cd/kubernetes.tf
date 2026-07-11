resource "kubernetes_namespace_v1" "this" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_secret_v1" "repository" {
  metadata {
    name      = "gitops-repository"
    namespace = kubernetes_namespace_v1.this.metadata[0].name

    labels = {
      "argocd.argoproj.io/secret-type" = "repository"
    }
  }

  data = {
    type     = "git"
    url      = var.gitops_repository_url
    username = "x-access-token"
    password = var.github_token
  }

  type = "Opaque"
}
