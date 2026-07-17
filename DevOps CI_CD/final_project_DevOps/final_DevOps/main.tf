module "s3_backend" {
  source = "./modules/s3-backend"

  bucket_name = var.state_bucket_name
  table_name  = var.state_lock_table_name

  tags = local.common_tags
}

module "vpc" {
  source = "./modules/vpc"

  name                    = local.name_prefix
  vpc_cidr                = var.vpc_cidr
  availability_zone_count = var.availability_zone_count
  enable_nat_gateway      = var.enable_nat_gateway
  single_nat_gateway      = var.single_nat_gateway

  tags = local.common_tags
}

module "ecr" {
  source = "./modules/ecr"

  repository_name       = var.ecr_repository_name
  image_retention_count = var.ecr_image_retention_count
  force_delete          = var.ecr_force_delete

  tags = local.common_tags
}

module "eks" {
  source = "./modules/eks"

  cluster_name         = var.eks_cluster_name
  kubernetes_version          = var.eks_kubernetes_version
  cluster_log_retention_days  = var.eks_cluster_log_retention_days
  vpc_id                      = module.vpc.vpc_id
  private_subnet_ids   = module.vpc.private_subnet_ids
  public_access_cidrs  = var.eks_public_access_cidrs
  node_instance_types  = var.eks_node_instance_types
  node_capacity_type   = var.eks_node_capacity_type
  node_desired_size    = var.eks_node_desired_size
  node_min_size        = var.eks_node_min_size
  node_max_size        = var.eks_node_max_size
  node_disk_size       = var.eks_node_disk_size

  tags = local.common_tags
}

module "rds" {
  source = "./modules/rds"

  name                        = "${local.name_prefix}-database"
  use_aurora                  = var.use_aurora
  engine                      = var.db_engine
  engine_version              = var.db_engine_version
  parameter_group_family      = var.db_parameter_group_family
  instance_class              = var.db_instance_class
  database_name               = var.db_name
  master_username             = var.db_username
  master_password             = var.db_password
  manage_master_user_password = var.db_manage_master_user_password
  multi_az                    = var.db_multi_az
  aurora_instance_count       = var.aurora_instance_count
  allocated_storage           = var.db_allocated_storage
  max_allocated_storage       = var.db_max_allocated_storage
  backup_retention_period     = var.db_backup_retention_period
  deletion_protection         = var.db_deletion_protection
  skip_final_snapshot         = var.db_skip_final_snapshot
  custom_parameters           = var.db_custom_parameters

  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids

  # The database is reachable only from EKS worker nodes by default.
  allowed_security_group_ids = [module.eks.node_security_group_id]
  allowed_cidr_blocks        = []

  tags = local.common_tags
}

module "jenkins" {
  source = "./modules/jenkins"

  providers = {
    kubernetes = kubernetes
    helm       = helm
    aws        = aws
    random     = random
  }

  namespace              = var.jenkins_namespace
  chart_version          = var.jenkins_chart_version
  cluster_name           = module.eks.cluster_name
  oidc_provider_arn      = module.eks.oidc_provider_arn
  oidc_provider_url      = module.eks.oidc_provider_url
  ecr_repository_arn     = module.ecr.repository_arn
  ecr_repository_url     = module.ecr.repository_url
  aws_region             = var.aws_region
  source_repository_url  = var.source_repository_url
  source_project_path    = var.source_project_path
  source_branch          = var.source_repository_branch
  jenkinsfile_path       = var.jenkinsfile_path
  gitops_repository_url  = var.gitops_repository_url
  gitops_branch          = var.gitops_repository_branch
  gitops_values_path     = var.gitops_values_path
  github_username        = var.github_username
  github_token           = var.github_token

  tags = local.common_tags

  depends_on = [module.eks, module.ecr]
}

module "monitoring" {
  source = "./modules/monitoring"

  providers = {
    kubernetes = kubernetes
    helm       = helm
    random     = random
  }

  namespace                     = var.monitoring_namespace
  kube_prometheus_chart_version = var.kube_prometheus_stack_chart_version
  metrics_server_chart_version  = var.metrics_server_chart_version

  depends_on = [module.eks]
}

module "argo_cd" {
  source = "./modules/argo_cd"

  providers = {
    kubernetes = kubernetes
    helm       = helm
    random     = random
  }

  namespace              = var.argocd_namespace
  chart_version          = var.argocd_chart_version
  repository_url         = var.gitops_repository_url
  repository_branch      = var.gitops_repository_branch
  repository_username    = var.github_username
  repository_password    = var.github_token
  application_chart_path = var.gitops_chart_path
  application_namespace  = "django-app"
  ecr_repository_url     = module.ecr.repository_url

  database_engine   = var.db_engine
  database_host     = module.rds.database_endpoint_address
  database_port     = module.rds.database_port
  database_name     = var.db_name
  database_username = var.db_username
  database_password = module.rds.database_password

  depends_on = [module.eks, module.rds, module.ecr, module.jenkins]
}
