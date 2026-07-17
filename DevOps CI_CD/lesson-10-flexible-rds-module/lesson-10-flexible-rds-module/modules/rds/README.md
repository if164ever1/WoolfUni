# Reusable RDS / Aurora Terraform module

This module creates either a standard Amazon RDS instance or an Amazon Aurora cluster from the same interface.

## Behavior

- `use_aurora = false`: creates one `aws_db_instance`.
- `use_aurora = true`: creates one `aws_rds_cluster` and `aurora_instance_count` cluster instances. Aurora automatically assigns the writer role to one healthy instance.
- Both modes create a DB subnet group, a private security group, and parameter groups.
- PostgreSQL receives `max_connections`, `log_statement`, and `work_mem` by default.
- MySQL receives compatible baseline parameters: `max_connections`, `slow_query_log`, and `long_query_time`.

## Example

```hcl
module "rds" {
  source = "./modules/rds"

  name                   = "my-project-dev-database"
  use_aurora             = false
  engine                 = "postgres"
  engine_version         = "16.3"
  parameter_group_family = "postgres16"
  instance_class         = "db.t3.micro"
  multi_az               = false

  database_name   = "appdb"
  master_username = "dbadmin"

  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids

  allowed_security_group_ids = []
  allowed_cidr_blocks        = []
}
```

## Switching engines

For standard MySQL, set `engine = "mysql"`, choose a MySQL-compatible `engine_version`, and use a matching family such as `mysql8.0`.

For Aurora, set `use_aurora = true`. The module maps `postgres` to `aurora-postgresql` and `mysql` to `aurora-mysql`; therefore the selected version and family must be Aurora-compatible.
