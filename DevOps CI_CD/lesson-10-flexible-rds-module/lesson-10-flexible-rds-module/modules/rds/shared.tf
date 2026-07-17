locals {
  database_port = var.engine == "postgres" ? 5432 : 3306
  aurora_engine = var.engine == "postgres" ? "aurora-postgresql" : "aurora-mysql"

  postgres_parameters = {
    max_connections = "200"
    log_statement   = "all"
    work_mem        = "4096"
  }

  mysql_parameters = {
    max_connections = "200"
    slow_query_log  = "1"
    long_query_time = "2"
  }

  base_parameters = var.engine == "postgres" ? local.postgres_parameters : local.mysql_parameters
  parameters      = merge(local.base_parameters, var.custom_parameters)

  final_snapshot_identifier = "${var.name}-final"
}

resource "aws_db_subnet_group" "this" {
  name       = "${var.name}-subnet-group"
  subnet_ids = var.private_subnet_ids

  tags = merge(var.tags, {
    Name = "${var.name}-subnet-group"
  })
}

resource "aws_security_group" "this" {
  name_prefix = "${var.name}-db-"
  description = "Database access for ${var.name}"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = toset(var.allowed_cidr_blocks)
    content {
      description = "Database access from ${ingress.value}"
      from_port   = local.database_port
      to_port     = local.database_port
      protocol    = "tcp"
      cidr_blocks = [ingress.value]
    }
  }

  dynamic "ingress" {
    for_each = toset(var.allowed_security_group_ids)
    content {
      description     = "Database access from security group ${ingress.value}"
      from_port       = local.database_port
      to_port         = local.database_port
      protocol        = "tcp"
      security_groups = [ingress.value]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.name}-database"
  })

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_db_parameter_group" "standard" {
  count = var.use_aurora ? 0 : 1

  name_prefix = "${var.name}-"
  family      = var.parameter_group_family
  description = "Managed parameter group for ${var.name}"

  dynamic "parameter" {
    for_each = local.parameters
    content {
      name         = parameter.key
      value        = parameter.value
      apply_method = "pending-reboot"
    }
  }

  tags = var.tags

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_rds_cluster_parameter_group" "aurora" {
  count = var.use_aurora ? 1 : 0

  name_prefix = "${var.name}-cluster-"
  family      = var.parameter_group_family
  description = "Managed Aurora cluster parameter group for ${var.name}"

  dynamic "parameter" {
    for_each = local.parameters
    content {
      name         = parameter.key
      value        = parameter.value
      apply_method = "pending-reboot"
    }
  }

  tags = var.tags

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_db_parameter_group" "aurora_instance" {
  count = var.use_aurora ? 1 : 0

  name_prefix = "${var.name}-instance-"
  family      = var.parameter_group_family
  description = "Aurora instance parameter group for ${var.name}"
  tags        = var.tags

  lifecycle {
    create_before_destroy = true
  }
}
