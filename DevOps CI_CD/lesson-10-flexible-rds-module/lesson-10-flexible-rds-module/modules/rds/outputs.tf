output "database_type" {
  description = "Selected deployment type: aurora or rds."
  value       = var.use_aurora ? "aurora" : "rds"
}

output "engine" {
  description = "Actual AWS engine name used by the database."
  value       = var.use_aurora ? local.aurora_engine : var.engine
}

output "endpoint" {
  description = "Primary database endpoint. For Aurora this is the writer endpoint."
  value       = var.use_aurora ? aws_rds_cluster.this[0].endpoint : aws_db_instance.this[0].address
}

output "reader_endpoint" {
  description = "Aurora reader endpoint, or null for standard RDS."
  value       = var.use_aurora ? aws_rds_cluster.this[0].reader_endpoint : null
}

output "port" {
  description = "Database TCP port."
  value       = local.database_port
}

output "database_name" {
  description = "Initial database name."
  value       = var.database_name
}

output "security_group_id" {
  description = "Security group ID attached to the database."
  value       = aws_security_group.this.id
}

output "db_subnet_group_name" {
  description = "Name of the DB subnet group."
  value       = aws_db_subnet_group.this.name
}

output "parameter_group_name" {
  description = "Main parameter group name used by standard RDS or the Aurora cluster."
  value       = var.use_aurora ? aws_rds_cluster_parameter_group.aurora[0].name : aws_db_parameter_group.standard[0].name
}

output "master_user_secret_arn" {
  description = "ARN of the AWS-managed master password secret, or null when password management is disabled."
  value = var.manage_master_user_password ? (
    var.use_aurora ? try(aws_rds_cluster.this[0].master_user_secret[0].secret_arn, null) : try(aws_db_instance.this[0].master_user_secret[0].secret_arn, null)
  ) : null
  sensitive = true
}
