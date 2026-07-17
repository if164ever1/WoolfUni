# Lesson 10 — Flexible Terraform module for RDS and Aurora

This project continues the infrastructure built in the previous Terraform, EKS, Helm, Jenkins, and Argo CD homework. The new component is a reusable `modules/rds` module that can create either a standard Amazon RDS database or an Amazon Aurora cluster by changing one flag.

## Project structure

```text
lesson-10-flexible-rds-module/
├── backend.tf
├── main.tf
├── outputs.tf
├── providers.tf
├── variables.tf
├── versions.tf
├── terraform.tfvars.example
├── modules/
│   ├── s3-backend/
│   ├── vpc/
│   ├── ecr/
│   ├── eks/
│   ├── rds/
│   │   ├── rds.tf
│   │   ├── aurora.tf
│   │   ├── shared.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── jenkins/
│   └── argo_cd/
└── charts/
    └── django-app/
```

## What the RDS module creates

With `use_aurora = false`:

- one `aws_db_instance`;
- one DB subnet group;
- one private database security group;
- one engine-compatible DB parameter group.

With `use_aurora = true`:

- one `aws_rds_cluster`;
- `aurora_instance_count` Aurora instances, with one instance serving as the writer;
- one DB subnet group;
- one private database security group;
- one Aurora cluster parameter group and one Aurora instance parameter group.

For PostgreSQL, the baseline parameters are `max_connections`, `log_statement`, and `work_mem`. MySQL does not support the PostgreSQL-only parameters, so the module uses compatible defaults: `max_connections`, `slow_query_log`, and `long_query_time`.

## Prerequisites

Install and authenticate Terraform and AWS CLI. The AWS account must have access to the services used by the project. The VPC inherited from the previous homework must already exist and contain private subnets matching `lesson-5-vpc-private-*`.

## 1. Clone and enter the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
```

## 2. Configure the backend

The project intentionally keeps the `s3_backend` module from the previous homework:

```hcl
module "s3_backend" {
  source = "./modules/s3-backend"

  bucket_name = var.state_bucket_name
  table_name  = var.state_lock_table_name
}
```

Update the bucket name in both `backend.tf` and `terraform.tfvars` so the values match your real backend resources.

When creating the backend resources for the first time:

```bash
terraform init -backend=false
terraform apply -target=module.s3_backend
terraform init -reconfigure
```

For later runs:

```bash
terraform init -reconfigure
```

## 3. Configure variables

Create your local variables file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

PowerShell:

```powershell
Copy-Item terraform.tfvars.example terraform.tfvars
```

The default configuration creates standard PostgreSQL RDS:

```hcl
use_aurora                = false
db_engine                 = "postgres"
db_engine_version         = "16.3"
db_parameter_group_family = "postgres16"
db_instance_class         = "db.t3.micro"
db_multi_az               = false
```

## 4. Validate and apply

```bash
terraform fmt -recursive
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
```

Useful outputs:

```bash
terraform output database_type
terraform output database_endpoint
terraform output database_port
terraform output database_security_group_id
```

## Example use of the module

```hcl
module "rds" {
  source = "./modules/rds"

  name                   = "lesson-10-dev-database"
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

  allowed_cidr_blocks        = []
  allowed_security_group_ids = []

  tags = {
    Project     = "lesson-10"
    Environment = "dev"
  }
}
```

## How to change the database type

### Standard PostgreSQL RDS

```hcl
use_aurora                = false
db_engine                 = "postgres"
db_engine_version         = "16.3"
db_parameter_group_family = "postgres16"
db_instance_class         = "db.t3.micro"
```

### Standard MySQL RDS

```hcl
use_aurora                = false
db_engine                 = "mysql"
db_engine_version         = "8.0"
db_parameter_group_family = "mysql8.0"
db_instance_class         = "db.t3.micro"
```

### Aurora PostgreSQL

```hcl
use_aurora                = true
db_engine                 = "postgres"
db_engine_version         = "16.3"
db_parameter_group_family = "aurora-postgresql16"
db_instance_class         = "db.r6g.large"
aurora_instance_count     = 1
```

### Aurora MySQL

```hcl
use_aurora                = true
db_engine                 = "mysql"
db_engine_version         = "8.0.mysql_aurora.3.08.0"
db_parameter_group_family = "aurora-mysql8.0"
db_instance_class         = "db.r6g.large"
aurora_instance_count     = 1
```

The chosen engine version, parameter group family, and instance class must be mutually compatible and available in the selected AWS region.

## Main variables

| Variable | Default | Description |
|---|---|---|
| `use_aurora` | `false` | Switches between standard RDS and Aurora. |
| `db_engine` | `postgres` | Logical engine: `postgres` or `mysql`. |
| `db_engine_version` | `16.3` | Selected engine version. |
| `db_parameter_group_family` | `postgres16` | Parameter family matching the selected engine/version. |
| `db_instance_class` | `db.t3.micro` | Compute class for standard RDS or Aurora instances. |
| `db_multi_az` | `false` | Enables Multi-AZ for standard RDS. |
| `aurora_instance_count` | `1` | Number of Aurora cluster instances. |
| `db_name` | `appdb` | Initial application database. |
| `db_username` | `dbadmin` | Master username. |
| `db_password` | `null` | Optional explicit password. |
| `manage_master_user_password` | `true` | Lets AWS manage the password in Secrets Manager. |
| `db_allocated_storage` | `20` | Standard RDS storage in GiB. |
| `db_max_allocated_storage` | `100` | RDS autoscaling maximum in GiB. |
| `db_storage_type` | `gp3` | Standard RDS storage type. |
| `rds_allowed_cidr_blocks` | `[]` | CIDRs allowed to reach the DB port. |
| `rds_allowed_security_group_ids` | `[]` | Security groups allowed to reach the DB. |
| `db_custom_parameters` | `{}` | Additional or overriding DB parameters. |
| `db_backup_retention_period` | `7` | Automated backup retention in days. |
| `db_deletion_protection` | `false` | Protects the database from deletion when enabled. |
| `db_skip_final_snapshot` | `true` | Skips the final snapshot in disposable environments. |
| `db_apply_immediately` | `true` | Applies modifications immediately. |

Every Terraform variable in the project includes a type, description, and default. Every output includes a description.

## Notes about credentials

By default, `manage_master_user_password = true`, so AWS RDS generates the master password and stores it in AWS Secrets Manager. This avoids committing a database password to Git or plain Terraform variables.

To manage the password yourself:

```hcl
manage_master_user_password = false
db_password                 = "REPLACE_WITH_A_SECURE_PASSWORD"
```

Never commit a real password in `terraform.tfvars`.

## Destroy

```bash
terraform plan -destroy -out=destroy.tfplan
terraform apply destroy.tfplan
```

The S3 bucket and DynamoDB table use `prevent_destroy = true` because they store Terraform state and locking information. Remove that protection only when you intentionally want to delete the backend after the main infrastructure is gone.
