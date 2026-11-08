resource "random_password" "master" {
  count = !var.manage_master_user_password && var.master_password == null ? 1 : 0

  length           = 24
  special          = true
  override_special = "!#$%&*+-=?_"
}

resource "aws_db_subnet_group" "this" {
  name       = "${var.name}-subnet-group"
  subnet_ids = var.private_subnet_ids

  tags = merge(var.tags, {
    Name = "${var.name}-subnet-group"
  })
}

resource "aws_security_group" "database" {
  name        = "${var.name}-sg"
  description = "Private database access"
  vpc_id      = var.vpc_id

  egress {
    description = "Allow database egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.name}-sg"
  })
}

resource "aws_vpc_security_group_ingress_rule" "from_security_groups" {
  for_each = toset(var.allowed_security_group_ids)

  security_group_id            = aws_security_group.database.id
  referenced_security_group_id = each.value
  ip_protocol                  = "tcp"
  from_port                    = local.db_port
  to_port                      = local.db_port
  description                  = "Allow database access from approved security group"
}

resource "aws_vpc_security_group_ingress_rule" "from_cidrs" {
  for_each = toset(var.allowed_cidr_blocks)

  security_group_id = aws_security_group.database.id
  cidr_ipv4         = each.value
  ip_protocol       = "tcp"
  from_port         = local.db_port
  to_port           = local.db_port
  description       = "Allow database access from approved CIDR"
}

resource "aws_db_parameter_group" "standard" {
  count = var.use_aurora ? 0 : 1

  name   = "${var.name}-params"
  family = var.parameter_group_family

  dynamic "parameter" {
    for_each = var.custom_parameters
    content {
      name  = parameter.key
      value = parameter.value
    }
  }

  tags = var.tags
}

resource "aws_rds_cluster_parameter_group" "aurora_cluster" {
  count = var.use_aurora ? 1 : 0

  name   = "${var.name}-cluster-params"
  family = var.parameter_group_family

  dynamic "parameter" {
    for_each = var.custom_parameters
    content {
      name  = parameter.key
      value = parameter.value
    }
  }

  tags = var.tags
}

resource "aws_db_parameter_group" "aurora_instance" {
  count = var.use_aurora ? 1 : 0

  name   = "${var.name}-instance-params"
  family = var.parameter_group_family

  tags = var.tags
}
