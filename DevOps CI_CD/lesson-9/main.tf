module "vpc" {
  source = "./modules/vpc"

  vpc_name     = var.existing_vpc_name
  cluster_name = var.cluster_name
}

module "ecr" {
  source = "./modules/ecr"

  repository_name = var.ecr_repository_name
}

module "eks" {
  source = "./modules/eks"

  cluster_name                 = var.cluster_name
  kubernetes_version           = var.kubernetes_version
  subnet_ids                   = module.vpc.private_subnet_ids
  endpoint_public_access_cidrs = var.cluster_endpoint_public_access_cidrs
  node_instance_types          = var.node_instance_types
  node_desired_size            = var.node_desired_size
  node_min_size                = var.node_min_size
  node_max_size                = var.node_max_size

  depends_on = [module.vpc]
}

module "jenkins" {
  source = "./modules/jenkins"

  namespace                   = var.jenkins_namespace
  chart_version               = var.jenkins_chart_version
  service_type                = var.jenkins_service_type
  admin_username              = var.jenkins_admin_username
  github_token                = var.github_token
  aws_region                  = var.aws_region
  ecr_repository_url          = module.ecr.repository_url
  ecr_repository_arn          = module.ecr.repository_arn
  oidc_provider_arn           = module.eks.oidc_provider_arn
  oidc_provider_url           = module.eks.oidc_provider_url
  source_repository_url       = var.source_repository_url
  source_repository_branch    = var.source_repository_branch
  jenkinsfile_path            = var.jenkinsfile_path
  gitops_repository_url       = var.gitops_repository_url
  gitops_repository_branch    = var.gitops_repository_branch
  gitops_values_file          = var.gitops_values_file
  agent_service_account_name  = "jenkins-agent"

  providers = {
    aws        = aws
    helm       = helm
    kubernetes = kubernetes
  }

  depends_on = [module.eks]
}

module "argo_cd" {
  source = "./modules/argo_cd"

  namespace                = var.argocd_namespace
  chart_version            = var.argocd_chart_version
  service_type             = var.argocd_service_type
  github_token             = var.github_token
  gitops_repository_url    = var.gitops_repository_url
  gitops_repository_branch = var.gitops_repository_branch
  application_namespace    = var.application_namespace
  application_name         = "django-app"
  chart_path               = "charts/django-app"

  providers = {
    helm       = helm
    kubernetes = kubernetes
  }

  depends_on = [module.eks, module.jenkins]
}
