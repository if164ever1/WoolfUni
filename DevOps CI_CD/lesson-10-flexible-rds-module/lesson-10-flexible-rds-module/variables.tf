variable "aws_region" {
  description = "AWS region used by all resources in this project."
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "Base project name used in resource names and tags."
  type        = string
  default     = "lesson-10"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"
}

variable "state_bucket_name" {
  description = "S3 bucket name used for Terraform remote state. Keep it aligned with backend.tf."
  type        = string
  default     = "your-name-terraform-state"
}

variable "state_lock_table_name" {
  description = "DynamoDB table name used for Terraform state locking. Keep it aligned with backend.tf."
  type        = string
  default     = "terraform-locks"
}

variable "existing_vpc_name" {
  description = "Name tag of the VPC inherited from the previous homework."
  type        = string
  default     = "lesson-5-vpc"
}

variable "public_subnet_name_pattern" {
  description = "Wildcard pattern used to discover public subnets in the existing VPC."
  type        = string
  default     = "lesson-5-vpc-public-*"
}

variable "private_subnet_name_pattern" {
  description = "Wildcard pattern used to discover private subnets used by EKS and RDS."
  type        = string
  default     = "lesson-5-vpc-private-*"
}

variable "enable_ecr" {
  description = "Whether to create the ECR module inherited from the previous homework."
  type        = bool
  default     = false
}

variable "ecr_repository_name" {
  description = "Name of the optional ECR repository."
  type        = string
  default     = "lesson-10-django"
}

variable "enable_eks" {
  description = "Whether to create the optional EKS module inherited from the previous homework."
  type        = bool
  default     = false
}

variable "cluster_name" {
  description = "Name of the optional EKS cluster."
  type        = string
  default     = "lesson-10-eks"
}

variable "node_instance_types" {
  description = "EC2 instance types used by the optional EKS managed node group."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "node_desired_size" {
  description = "Desired number of worker nodes in the optional EKS node group."
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "Minimum number of worker nodes in the optional EKS node group."
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Maximum number of worker nodes in the optional EKS node group."
  type        = number
  default     = 3
}

variable "use_aurora" {
  description = "When true, creates an Aurora cluster; when false, creates one standard RDS instance."
  type        = bool
  default     = false
}

variable "db_engine" {
  description = "Logical database engine. Supported values are postgres and mysql."
  type        = string
  default     = "postgres"

  validation {
    condition     = contains(["postgres", "mysql"], var.db_engine)
    error_message = "db_engine must be either postgres or mysql."
  }
}

variable "db_engine_version" {
  description = "Database engine version. The value must be compatible with the selected engine and parameter group family."
  type        = string
  default     = "16.3"
}

variable "db_parameter_group_family" {
  description = "RDS parameter group family matching the selected engine and major version."
  type        = string
  default     = "postgres16"
}

variable "db_instance_class" {
  description = "Instance class used by standard RDS or each Aurora cluster instance."
  type        = string
  default     = "db.t3.micro"
}

variable "db_multi_az" {
  description = "Whether a standard RDS instance uses Multi-AZ deployment. Ignored for Aurora."
  type        = bool
  default     = false
}

variable "db_name" {
  description = "Name of the initial application database."
  type        = string
  default     = "appdb"
}

variable "db_username" {
  description = "Master database username."
  type        = string
  default     = "dbadmin"
}

variable "db_password" {
  description = "Optional master password. Keep null when AWS Secrets Manager should manage the master password."
  type        = string
  default     = null
  sensitive   = true
}

variable "manage_master_user_password" {
  description = "Whether AWS RDS should generate and manage the master password in AWS Secrets Manager."
  type        = bool
  default     = true
}

variable "db_allocated_storage" {
  description = "Initial storage in GiB for standard RDS. Ignored for Aurora."
  type        = number
  default     = 20
}

variable "db_max_allocated_storage" {
  description = "Maximum storage autoscaling threshold in GiB for standard RDS. Set 0 to disable autoscaling."
  type        = number
  default     = 100
}

variable "db_storage_type" {
  description = "Storage type for standard RDS. Ignored for Aurora."
  type        = string
  default     = "gp3"
}

variable "aurora_instance_count" {
  description = "Number of Aurora instances. The first available instance acts as the writer."
  type        = number
  default     = 1

  validation {
    condition     = var.aurora_instance_count >= 1
    error_message = "aurora_instance_count must be at least 1."
  }
}

variable "rds_allowed_cidr_blocks" {
  description = "CIDR blocks allowed to connect to the database port. Empty by default for private-only access."
  type        = list(string)
  default     = []
}

variable "rds_allowed_security_group_ids" {
  description = "Security group IDs allowed to connect to the database port, for example an EKS node or application security group."
  type        = list(string)
  default     = []
}

variable "db_custom_parameters" {
  description = "Additional or overriding parameter-group values. Keys are parameter names and values are strings."
  type        = map(string)
  default     = {}
}

variable "db_backup_retention_period" {
  description = "Number of days to retain automated database backups."
  type        = number
  default     = 7
}

variable "db_deletion_protection" {
  description = "Whether deletion protection is enabled for the database."
  type        = bool
  default     = false
}

variable "db_skip_final_snapshot" {
  description = "Whether to skip the final snapshot when destroying the database. Suitable for disposable homework environments."
  type        = bool
  default     = true
}

variable "db_apply_immediately" {
  description = "Whether database modifications are applied immediately instead of during the maintenance window."
  type        = bool
  default     = true
}
