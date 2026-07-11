resource "random_password" "admin" {
  length           = 24
  special          = true
  override_special = "!@#%_-"
}

locals {
  job_dsl = templatefile("${path.module}/job.groovy.tpl", {
    source_repository_url    = var.source_repository_url
    source_repository_branch = var.source_repository_branch
    jenkinsfile_path         = var.jenkinsfile_path
  })

  credentials_jcasc = yamlencode({
    credentials = {
      system = {
        domainCredentials = [
          {
            credentials = [
              {
                usernamePassword = {
                  scope       = "GLOBAL"
                  id          = "github-pat"
                  username    = "x-access-token"
                  password    = "$${GITHUB_TOKEN}"
                  description = "GitHub token managed by Terraform"
                }
              }
            ]
          }
        ]
      }
    }
  })

  job_jcasc = yamlencode({
    jobs = [
      {
        script = local.job_dsl
      }
    ]
  })

  global_env_jcasc = yamlencode({
    jenkins = {
      globalNodeProperties = [
        {
          envVars = {
            env = [
              { key = "AWS_REGION", value = var.aws_region },
              { key = "ECR_REPOSITORY_URI", value = var.ecr_repository_url },
              { key = "GITOPS_REPO_URL", value = var.gitops_repository_url },
              { key = "GITOPS_BRANCH", value = var.gitops_repository_branch },
              { key = "GITOPS_VALUES_FILE", value = var.gitops_values_file }
            ]
          }
        }
      ]
    }
  })

  dynamic_values = {
    controller = {
      serviceType = var.service_type
      admin = {
        username     = var.admin_username
        password     = random_password.admin.result
        createSecret = true
      }
      containerEnv = [
        {
          name = "GITHUB_TOKEN"
          valueFrom = {
            secretKeyRef = {
              name = kubernetes_secret_v1.github.metadata[0].name
              key  = "github-token"
            }
          }
        }
      ]
      JCasC = {
        defaultConfig          = true
        overwriteConfiguration = true
        configScripts = {
          "github-credentials" = local.credentials_jcasc
          "pipeline-job"       = local.job_jcasc
          "global-environment" = local.global_env_jcasc
        }
      }
    }
    serviceAccountAgent = {
      create = true
      name   = var.agent_service_account_name
      annotations = {
        "eks.amazonaws.com/role-arn" = aws_iam_role.agent.arn
      }
      automountServiceAccountToken = true
    }
    agent = {
      enabled        = true
      serviceAccount = var.agent_service_account_name
    }
  }
}

resource "helm_release" "jenkins" {
  name       = "jenkins"
  namespace  = kubernetes_namespace_v1.this.metadata[0].name
  repository = "https://charts.jenkins.io"
  chart      = "jenkins"
  version    = var.chart_version

  atomic          = true
  cleanup_on_fail = true
  timeout         = 1200
  wait            = true

  values = [
    file("${path.module}/values.yaml"),
    yamlencode(local.dynamic_values)
  ]

  depends_on = [
    kubernetes_storage_class_v1.jenkins_gp3,
    kubernetes_secret_v1.github,
    aws_iam_role_policy_attachment.ecr_push
  ]
}
