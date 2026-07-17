output "s3_bucket_name" {
  description = "Name of the S3 bucket used for Terraform state."
  value       = module.s3_backend.bucket_name
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table used for Terraform state locking."
  value       = module.s3_backend.dynamodb_table_name
}

output "vpc_id" {
  description = "ID of the existing VPC reused by this project."
  value       = module.vpc.vpc_id
}

output "private_subnet_ids" {
  description = "Private subnet IDs used by the database module."
  value       = module.vpc.private_subnet_ids
}

output "database_type" {
  description = "Database deployment type selected by use_aurora."
  value       = module.rds.database_type
}

output "database_engine" {
  description = "Actual AWS database engine used by the selected deployment type."
  value       = module.rds.engine
}

output "database_endpoint" {
  description = "Primary database endpoint. For Aurora this is the cluster writer endpoint."
  value       = module.rds.endpoint
}

output "database_reader_endpoint" {
  description = "Aurora reader endpoint, or null for standard RDS."
  value       = module.rds.reader_endpoint
}

output "database_port" {
  description = "TCP port used by the selected database engine."
  value       = module.rds.port
}

output "database_name" {
  description = "Initial application database name."
  value       = module.rds.database_name
}

output "database_security_group_id" {
  description = "Security group ID attached to the database."
  value       = module.rds.security_group_id
}

output "database_subnet_group_name" {
  description = "DB subnet group name used by RDS or Aurora."
  value       = module.rds.db_subnet_group_name
}

output "database_parameter_group_name" {
  description = "Main parameter group name used by the selected database deployment."
  value       = module.rds.parameter_group_name
}

output "database_master_user_secret_arn" {
  description = "ARN of the AWS-managed master user secret when manage_master_user_password is enabled."
  value       = module.rds.master_user_secret_arn
  sensitive   = true
}
