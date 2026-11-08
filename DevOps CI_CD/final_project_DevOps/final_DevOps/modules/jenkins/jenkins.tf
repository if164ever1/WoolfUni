resource "random_password" "admin" {
  length           = 24
  special          = true
  override_special = "!#$%&*+-=?_"
}

resource "kubernetes_namespace_v1" "this" {
  metadata {
    name = var.namespace
  }
}

locals {
  service_account_name = "jenkins-agent"
}

data "aws_iam_policy_document" "agent_assume" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    principals {
      type        = "Federated"
      identifiers = [var.oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${var.oidc_provider_url}:sub"
      values   = ["system:serviceaccount:${var.namespace}:${local.service_account_name}"]
    }

    condition {
      test     = "StringEquals"
      variable = "${var.oidc_provider_url}:aud"
      values   = ["sts.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "agent" {
  name               = "${var.cluster_name}-jenkins-agent-role"
  assume_role_policy = data.aws_iam_policy_document.agent_assume.json
  tags               = var.tags
}

data "aws_iam_policy_document" "ecr" {
  statement {
    sid       = "ECRAuthorization"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  statement {
    sid = "ECRRepositoryAccess"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:CompleteLayerUpload",
      "ecr:GetDownloadUrlForLayer",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart",
      "ecr:BatchGetImage"
    ]
    resources = [var.ecr_repository_arn]
  }
}

resource "aws_iam_role_policy" "ecr" {
  name   = "ecr-push"
  role   = aws_iam_role.agent.id
  policy = data.aws_iam_policy_document.ecr.json
}

resource "kubernetes_service_account_v1" "agent" {
  metadata {
    name      = local.service_account_name
    namespace = kubernetes_namespace_v1.this.metadata[0].name

    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.agent.arn
    }
  }
}

resource "kubernetes_secret_v1" "github" {
  metadata {
    name      = "jenkins-github-token"
    namespace = kubernetes_namespace_v1.this.metadata[0].name
  }

  data = {
    username = var.github_username
    token    = var.github_token
  }

  type = "Opaque"
}

resource "helm_release" "jenkins" {
  name       = "jenkins"
  namespace  = kubernetes_namespace_v1.this.metadata[0].name
  repository = "https://charts.jenkins.io"
  chart      = "jenkins"
  version    = var.chart_version

  timeout         = 900
  wait            = true
  cleanup_on_fail = true

  values = [
    templatefile("${path.module}/values.yaml", {
      admin_username          = var.admin_username
      admin_password          = random_password.admin.result
      github_secret_name      = kubernetes_secret_v1.github.metadata[0].name
      source_repository_url   = var.source_repository_url
      source_project_path     = var.source_project_path
      source_branch           = var.source_branch
      jenkinsfile_path        = var.jenkinsfile_path
      ecr_repository_url      = var.ecr_repository_url
      aws_region              = var.aws_region
      gitops_repository_url   = var.gitops_repository_url
      gitops_branch           = var.gitops_branch
      gitops_values_path      = var.gitops_values_path
      agent_service_account   = kubernetes_service_account_v1.agent.metadata[0].name
    })
  ]

  depends_on = [
    kubernetes_service_account_v1.agent,
    kubernetes_secret_v1.github,
    aws_iam_role_policy.ecr
  ]
}
