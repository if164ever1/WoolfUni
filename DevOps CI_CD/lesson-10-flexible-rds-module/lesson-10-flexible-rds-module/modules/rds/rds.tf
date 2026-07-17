resource "aws_db_instance" "this" {
  count = var.use_aurora ? 0 : 1

  identifier = var.name

  engine         = var.engine
  engine_version = var.engine_version
  instance_class = var.instance_class

  db_name  = var.database_name
  username = var.master_username
  password = var.manage_master_user_password ? null : var.master_password

  manage_master_user_password = var.manage_master_user_password

  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  storage_type          = var.storage_type
  storage_encrypted     = true

  port                   = local.database_port
  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.this.id]
  parameter_group_name   = aws_db_parameter_group.standard[0].name

  multi_az            = var.multi_az
  publicly_accessible = false

  backup_retention_period = var.backup_retention_period
  deletion_protection      = var.deletion_protection
  skip_final_snapshot      = var.skip_final_snapshot
  final_snapshot_identifier = var.skip_final_snapshot ? null : local.final_snapshot_identifier

  auto_minor_version_upgrade = true
  apply_immediately          = var.apply_immediately
  copy_tags_to_snapshot      = true

  tags = var.tags
}
