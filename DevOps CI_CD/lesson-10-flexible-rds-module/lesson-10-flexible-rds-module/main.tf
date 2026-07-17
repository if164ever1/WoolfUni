module "s3_backend" {
  source = "./modules/s3-backend"

  bucket_name = var.state_bucket_name
  table_name  = var.state_lock_table_name
}

module "vpc" {
  source = "./modules/vpc"

  existing_vpc_name          = var.existing_vpc_name
  public_subnet_name_pattern = var.public_subnet_name_pattern
  private_subnet_name_pattern = var.private_subnet_name_pattern
}

module "ecr" {
  count  = var.enable_ecr ? 1 : 0
  source = "./modules/ecr"

  repository_name = var.ecr_repository_name
}

module "eks" {
  count  = var.enable_eks ? 1 : 0
  source = "./modules/eks"

  cluster_name       = var.cluster_name
  private_subnet_ids = module.vpc.private_subnet_ids
  instance_types     = var.node_instance_types
  desired_size       = var.node_desired_size
  min_size           = var.node_min_size
  max_size           = var.node_max_size
}

module "rds" {
  source = "./modules/rds"

  name                   = "${var.project_name}-${var.environment}-database"
  use_aurora             = var.use_aurora
  engine                 = var.db_engine
  engine_version         = var.db_engine_version
  parameter_group_family = var.db_parameter_group_family
  instance_class         = var.db_instance_class
  multi_az               = var.db_multi_az

  database_name          = var.db_name
  master_username        = var.db_username
  master_password        = var.db_password
  manage_master_user_password = var.manage_master_user_password

  allocated_storage      = var.db_allocated_storage
  max_allocated_storage  = var.db_max_allocated_storage
  storage_type           = var.db_storage_type
  aurora_instance_count  = var.aurora_instance_count

  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids

  allowed_cidr_blocks        = var.rds_allowed_cidr_blocks
  allowed_security_group_ids = var.rds_allowed_security_group_ids
  custom_parameters          = var.db_custom_parameters

  backup_retention_period = var.db_backup_retention_period
  deletion_protection      = var.db_deletion_protection
  skip_final_snapshot      = var.db_skip_final_snapshot
  apply_immediately        = var.db_apply_immediately

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
