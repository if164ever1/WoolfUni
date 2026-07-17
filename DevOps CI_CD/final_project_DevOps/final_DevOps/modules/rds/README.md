# RDS/Aurora module

This reusable module creates either a standard Amazon RDS instance or an Amazon Aurora cluster.
Set `use_aurora = false` for standard PostgreSQL/MySQL RDS and `use_aurora = true` for Aurora.
The module always creates a private DB subnet group and a security group, encrypts storage, and supports either an AWS-managed master password or a Terraform-generated password.
