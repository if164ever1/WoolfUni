# Lesson 5 — Terraform Infrastructure on AWS

This project provisions core AWS infrastructure using Terraform with a modular structure.  
It covers remote state management (S3 + DynamoDB), networking (VPC), and a container registry (ECR).

---

## Project Structure

```
lesson-5/
│
├── main.tf          # Root module — Terraform/provider config + module wiring
├── backend.tf       # Remote state backend (S3 + DynamoDB)
├── variables.tf     # Root-level variables (region, environment)
├── outputs.tf       # Aggregated outputs from all modules
│
├── modules/
│   ├── s3-backend/  # S3 bucket + DynamoDB for Terraform state
│   │   ├── s3.tf
│   │   ├── dynamodb.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   ├── vpc/         # VPC, subnets, IGW, NAT, route tables
│   │   ├── vpc.tf
│   │   ├── routes.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   └── ecr/         # ECR repository with scanning and lifecycle policy
│       ├── ecr.tf
│       ├── variables.tf
│       └── outputs.tf
│
└── README.md
```

---

## Modules

### Root configuration (`main.tf`)
Defines the required Terraform version, the AWS provider version constraint, and default tags applied to every resource created in this project.

```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "DevOps-Training"
      ManagedBy   = "Terraform"
      Environment = var.environment
    }
  }
}
```

**Root variables:**

| Name | Type | Default | Description |
|---|---|---|---|
| `aws_region` | `string` | `us-west-2` | AWS region used by the provider |
| `environment` | `string` | `dev` | Environment tag applied to all resources |

### `s3-backend`
Creates the S3 bucket and DynamoDB table used as the Terraform remote backend.

| Resource | Description |
|---|---|
| `aws_s3_bucket` | Stores `terraform.tfstate` files |
| `aws_s3_bucket_versioning` | Keeps history of all state versions |
| `aws_s3_bucket_server_side_encryption_configuration` | AES256 encryption at rest |
| `aws_s3_bucket_public_access_block` | Blocks all public access |
| `aws_dynamodb_table` | Provides state locking to prevent concurrent `apply` conflicts |

**Variables:**

| Name | Type | Description |
|---|---|---|
| `bucket_name` | `string` | Unique S3 bucket name |
| `table_name` | `string` | DynamoDB table name (default: `terraform-locks`) |

---

### `vpc`
Creates a full network environment with public and private subnets across 3 availability zones.

| Resource | Description |
|---|---|
| `aws_vpc` | Main VPC with DNS support enabled |
| `aws_subnet` (public ×3) | Public subnets with auto-assigned public IPs |
| `aws_subnet` (private ×3) | Private subnets without public IP assignment |
| `aws_internet_gateway` | Allows public subnets to reach the internet |
| `aws_nat_gateway` (×3) | Allows private subnets to initiate outbound internet traffic |
| `aws_route_table` | Separate route tables for public and private subnets |

**Variables:**

| Name | Type | Description |
|---|---|---|
| `vpc_cidr_block` | `string` | VPC CIDR (e.g. `10.0.0.0/16`) |
| `public_subnets` | `list(string)` | List of 3 public subnet CIDRs |
| `private_subnets` | `list(string)` | List of 3 private subnet CIDRs |
| `availability_zones` | `list(string)` | List of 3 AZs |
| `vpc_name` | `string` | Name tag prefix for all resources |

---

### `ecr`
Creates an Elastic Container Registry repository for storing Docker images.

| Resource | Description |
|---|---|
| `aws_ecr_repository` | Repository with AES256 encryption |
| `aws_ecr_lifecycle_policy` | Keeps the last 10 images, removes older ones |
| `aws_ecr_repository_policy` | Grants push/pull access to the AWS account root |

**Variables:**

| Name | Type | Description |
|---|---|---|
| `ecr_name` | `string` | Name of the ECR repository |
| `scan_on_push` | `bool` | Enable image vulnerability scanning (default: `true`) |

---

## Usage

### Prerequisites
- [Terraform](https://developer.hashicorp.com/terraform/downloads) >= 1.0
- AWS CLI configured (`aws configure`)
- Sufficient IAM permissions (S3, DynamoDB, VPC, ECR)

### ⚠️ First-time bootstrap

The S3 backend must exist **before** Terraform can use it.  
On the very first run, comment out `backend.tf`, apply once to create the bucket, then uncomment and run `terraform init` again to migrate state.

### Commands

```bash
# Initialize Terraform and download providers
terraform init

# Preview the execution plan
terraform plan

# Apply changes and provision infrastructure
terraform apply

# Destroy all resources when done (important — avoids unexpected AWS costs!)
terraform destroy
```

### After `terraform apply`, the following outputs are shown:

| Output | Description |
|---|---|
| `s3_bucket_name` | Name of the state S3 bucket |
| `s3_bucket_arn` | ARN of the S3 bucket |
| `dynamodb_table_name` | DynamoDB lock table name |
| `vpc_id` | ID of the created VPC |
| `public_subnet_ids` | IDs of public subnets |
| `private_subnet_ids` | IDs of private subnets |
| `ecr_repository_url` | Docker push/pull URL for ECR |
| `ecr_repository_arn` | ARN of the ECR repository |

---

## Important Notes

> **Cost warning:** NAT Gateways are billed per hour and per GB of data processed.  
> Always run `terraform destroy` after testing to avoid unexpected charges.

> **State locking:** DynamoDB ensures only one `terraform apply` runs at a time,  
> preventing state corruption in team environments.
