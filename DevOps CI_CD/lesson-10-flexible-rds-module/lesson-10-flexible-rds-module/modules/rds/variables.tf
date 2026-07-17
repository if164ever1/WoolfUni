variable "name" {
  description = "Base name used for RDS/Aurora resources."
  type        = string
  default     = "app-database"
}

variable "use_aurora" {
  description = "Creates Aurora when true and one standard RDS instance when false."
  type        = bool
  default     = false
}

variable "engine" {
  description = "Logical database engine: postgres or mysql. Aurora engine names are mapped automatically."
  type        = string
  default     = "postgres"

  validation {
    condition     = contains(["postgres", "mysql"], var.engine)
    error_message = "engine must be postgres or mysql."
  }
}

variable "engine_version" {
  description = "Engine version compatible with the selected RDS or Aurora engine."
  type        = string
  default     = "16.3"
}

variable "parameter_group_family" {
  description = "Parameter group family compatible with the selected engine and major version."
  type        = string
  default     = "postgres16"
}

variable "instance_class" {
  description = "Database instance class. Used by standard RDS and Aurora cluster instances."
  type        = string
  default     = "db.t3.micro"
}

variable "multi_az" {
  description = "Enables Multi-AZ for standard RDS. Aurora provides cluster-level high availability instead."
  type        = bool
  default     = false
}

variable "database_name" {
  description = "Name of the initial database."
  type        = string
  default     = "appdb"
}

variable "master_username" {
  description = "Master database username."
  type        = string
  default     = "dbadmin"
}

variable "master_password" {
  description = "Optional master password. Must be null when manage_master_user_password is true."
  type        = string
  default     = null
  sensitive   = true
}

variable "manage_master_user_password" {
  description = "Lets AWS RDS generate and store the master password in AWS Secrets Manager."
  type        = bool
  default     = true
}

variable "vpc_id" {
  description = "VPC ID where the database security group is created."
  type        = string
  default     = ""
}

variable "private_subnet_ids" {
  description = "Private subnet IDs used to build the DB subnet group. At least two Availability Zones are recommended and required for Aurora."
  type        = list(string)
  default     = []
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to connect to the database port."
  type        = list(string)
  default     = []
}

variable "allowed_security_group_ids" {
  description = "Source security groups allowed to connect to the database port."
  type        = list(string)
  default     = []
}

variable "allocated_storage" {
  description = "Initial storage in GiB for standard RDS. Ignored by Aurora."
  type        = number
  default     = 20
}

variable "max_allocated_storage" {
  description = "Maximum autoscaled storage in GiB for standard RDS. Set 0 to disable autoscaling."
  type        = number
  default     = 100
}

variable "storage_type" {
  description = "Storage type used by standard RDS. Ignored by Aurora."
  type        = string
  default     = "gp3"
}

variable "aurora_instance_count" {
  description = "Number of Aurora cluster instances. The cluster elects one writer; remaining instances can serve as readers."
  type        = number
  default     = 1

  validation {
    condition     = var.aurora_instance_count >= 1
    error_message = "aurora_instance_count must be at least 1."
  }
}

variable "custom_parameters" {
  description = "Additional or overriding DB parameters. Values are supplied as strings."
  type        = map(string)
  default     = {}
}

variable "backup_retention_period" {
  description = "Number of days to retain automated backups."
  type        = number
  default     = 7
}

variable "deletion_protection" {
  description = "Whether deletion protection is enabled."
  type        = bool
  default     = false
}

variable "skip_final_snapshot" {
  description = "Whether to skip a final snapshot when the database is destroyed."
  type        = bool
  default     = true
}

variable "apply_immediately" {
  description = "Whether database changes are applied immediately."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Additional tags applied to all taggable database resources."
  type        = map(string)
  default     = {}
}
