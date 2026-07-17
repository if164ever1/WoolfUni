$ErrorActionPreference = "Stop"

function Invoke-Terraform {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments)
    & terraform @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Terraform command failed: terraform $($Arguments -join ' ')"
    }
}

Write-Host "1/6 - Checking required CLI tools"
foreach ($command in @("terraform", "aws", "kubectl", "helm")) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "$command is not installed or is not available in PATH."
    }
}

if (-not (Test-Path "terraform.tfvars")) {
    Copy-Item "terraform.tfvars.example" "terraform.tfvars"
    throw "terraform.tfvars was created from the example. Edit the repository URLs and globally unique S3 bucket name, then run this script again."
}

Write-Host "2/6 - Bootstrapping the S3/DynamoDB backend with local Terraform state"
Invoke-Terraform init -backend=false -reconfigure
Invoke-Terraform apply -target=module.s3_backend -auto-approve

$bucket = (& terraform output -raw terraform_state_bucket).Trim()
$table  = (& terraform output -raw terraform_lock_table).Trim()
$region = (& terraform output -raw aws_region).Trim()

@"
bucket         = "$bucket"
key            = "final-project/terraform.tfstate"
region         = "$region"
dynamodb_table = "$table"
encrypt        = true
"@ | Set-Content -Path "backend.hcl" -Encoding UTF8

Write-Host "3/6 - Migrating local state into the remote backend"
Invoke-Terraform init -migrate-state -force-copy -backend-config=backend.hcl -reconfigure

Write-Host "4/6 - Creating AWS infrastructure required before Kubernetes/Helm providers"
Invoke-Terraform apply `
    -target=module.vpc `
    -target=module.ecr `
    -target=module.eks `
    -target=module.rds `
    -auto-approve

$cluster = (& terraform output -raw cluster_name).Trim()
Write-Host "5/6 - Configuring kubectl for $cluster"
& aws eks update-kubeconfig --region $region --name $cluster
if ($LASTEXITCODE -ne 0) { throw "aws eks update-kubeconfig failed." }
& kubectl get nodes
if ($LASTEXITCODE -ne 0) { throw "kubectl cannot reach the EKS cluster." }

Write-Host "6/6 - Running the complete Terraform deployment"
Invoke-Terraform plan -out=tfplan
Invoke-Terraform apply tfplan

Write-Host "Deployment complete. Run .\scripts\verify.ps1 for the acceptance checks."
