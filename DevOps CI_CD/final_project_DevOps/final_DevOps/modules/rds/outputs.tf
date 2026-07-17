output "database_type" {
  description = "Database deployment type."
  value       = var.use_aurora ? "Aurora" : "RDS"
}

output "database_endpoint" {
  description = "Database endpoint with port."
  value = var.use_aurora ? (
    "${aws_rds_cluster.this[0].endpoint}:${local.db_port}"
  ) : (
    aws_db_instance.this[0].endpoint
  )
}

output "database_endpoint_address" {
  description = "Database hostname without a port suffix."
  value = var.use_aurora ? (
    aws_rds_cluster.this[0].endpoint
  ) : (
    aws_db_instance.this[0].address
  )
}

output "database_port" {
  description = "Database TCP port."
  value       = local.db_port
}

output "database_name" {
  description = "Initial application database name."
  value       = var.database_name
}

output "database_username" {
  description = "Database master username."
  value       = var.master_username
}

output "database_password" {
  description = "Terraform-managed database password, or null when AWS manages it in Secrets Manager."
  value       = local.generated_password
  sensitive   = true
}

output "database_security_group_id" {
  description = "Security group attached to the database."
  value       = aws_security_group.database.id
}

output "master_user_secret_arn" {
  description = "AWS Secrets Manager secret ARN when manage_master_user_password is enabled."
  value = try(
    var.use_aurora ? aws_rds_cluster.this[0].master_user_secret[0].secret_arn : aws_db_instance.this[0].master_user_secret[0].secret_arn,
    null
  )
}
