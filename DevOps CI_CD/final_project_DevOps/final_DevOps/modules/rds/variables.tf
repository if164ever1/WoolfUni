variable "name" {
  description = "Name prefix for database resources."
  type        = string
  default     = "final-devops-dev-database"
}

variable "use_aurora" {
  description = "Create Aurora when true; otherwise create standard RDS."
  type        = bool
  default     = false
}

variable "engine" {
  description = "Logical engine: postgres or mysql."
  type        = string
  default     = "postgres"

  validation {
    condition     = contains(["postgres", "mysql"], var.engine)
    error_message = "engine must be either postgres or mysql."
  }
}

variable "engine_version" {
  description = "Database engine version."
  type        = string
  default     = "16.3"
}

variable "parameter_group_family" {
  description = "DB parameter group family compatible with the selected engine version."
  type        = string
  default     = "postgres16"
}

variable "instance_class" {
  description = "RDS/Aurora DB instance class."
  type        = string
  default     = "db.t3.micro"
}

variable "database_name" {
  description = "Initial database name."
  type        = string
  default     = "appdb"
}

variable "master_username" {
  description = "Database master username."
  type        = string
  default     = "dbadmin"
}

variable "master_password" {
  description = "Optional explicit master password."
  type        = string
  default     = null
  sensitive   = true
}

variable "manage_master_user_password" {
  description = "Let AWS Secrets Manager manage the master password."
  type        = bool
  default     = false
}

variable "multi_az" {
  description = "Enable Multi-AZ for standard RDS."
  type        = bool
  default     = false
}

variable "aurora_instance_count" {
  description = "Number of Aurora instances."
  type        = number
  default     = 1
}

variable "allocated_storage" {
  description = "Initial standard RDS storage in GiB."
  type        = number
  default     = 20
}

variable "max_allocated_storage" {
  description = "Maximum standard RDS autoscaled storage in GiB."
  type        = number
  default     = 100
}

variable "storage_type" {
  description = "Standard RDS storage type."
  type        = string
  default     = "gp3"
}

variable "backup_retention_period" {
  description = "Automated backup retention period in days."
  type        = number
  default     = 7
}

variable "deletion_protection" {
  description = "Enable database deletion protection."
  type        = bool
  default     = false
}

variable "skip_final_snapshot" {
  description = "Skip final snapshot on deletion."
  type        = bool
  default     = true
}

variable "apply_immediately" {
  description = "Apply database changes immediately."
  type        = bool
  default     = true
}

variable "vpc_id" {
  description = "VPC ID containing the database."
  type        = string
  default     = ""
}

variable "private_subnet_ids" {
  description = "Private subnet IDs used by the DB subnet group."
  type        = list(string)
  default     = []
}

variable "allowed_security_group_ids" {
  description = "Security groups allowed to connect to the database port."
  type        = list(string)
  default     = []
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to connect to the database port."
  type        = list(string)
  default     = []
}

variable "custom_parameters" {
  description = "Additional DB parameters compatible with the selected engine."
  type        = map(string)
  default     = {}
}

variable "tags" {
  description = "Tags applied to database resources."
  type        = map(string)
  default     = {}
}
