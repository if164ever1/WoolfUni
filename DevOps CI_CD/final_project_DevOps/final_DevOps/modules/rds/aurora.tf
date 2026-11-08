resource "aws_rds_cluster" "this" {
  count = var.use_aurora ? 1 : 0

  cluster_identifier = var.name

  engine         = local.aurora_engine
  engine_version = var.engine_version

  database_name   = var.database_name
  master_username = var.master_username
  master_password = var.manage_master_user_password ? null : local.generated_password

  manage_master_user_password = var.manage_master_user_password

  port                            = local.db_port
  db_subnet_group_name            = aws_db_subnet_group.this.name
  vpc_security_group_ids          = [aws_security_group.database.id]
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.aurora_cluster[0].name

  storage_encrypted        = true
  backup_retention_period  = var.backup_retention_period
  deletion_protection      = var.deletion_protection
  skip_final_snapshot      = var.skip_final_snapshot
  apply_immediately        = var.apply_immediately
  copy_tags_to_snapshot    = true

  tags = merge(var.tags, {
    Name = var.name
  })
}

resource "aws_rds_cluster_instance" "this" {
  count = var.use_aurora ? var.aurora_instance_count : 0

  identifier         = "${var.name}-${count.index + 1}"
  cluster_identifier = aws_rds_cluster.this[0].id
  instance_class     = var.instance_class
  engine             = aws_rds_cluster.this[0].engine
  engine_version     = aws_rds_cluster.this[0].engine_version

  db_parameter_group_name = aws_db_parameter_group.aurora_instance[0].name
  publicly_accessible     = false

  tags = var.tags
}
