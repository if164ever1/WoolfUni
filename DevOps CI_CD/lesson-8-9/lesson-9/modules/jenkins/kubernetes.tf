resource "kubernetes_namespace_v1" "this" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_storage_class_v1" "jenkins_gp3" {
  metadata {
    name = "jenkins-gp3"
  }

  storage_provisioner = "ebs.csi.aws.com"
  reclaim_policy      = "Delete"
  volume_binding_mode = "WaitForFirstConsumer"

  parameters = {
    type      = "gp3"
    encrypted = "true"
    fsType    = "ext4"
  }
}

resource "kubernetes_secret_v1" "github" {
  metadata {
    name      = "jenkins-github-token"
    namespace = kubernetes_namespace_v1.this.metadata[0].name
  }

  data = {
    github-token = var.github_token
  }

  type = "Opaque"
}
