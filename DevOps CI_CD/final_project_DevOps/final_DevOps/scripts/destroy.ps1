$ErrorActionPreference = "Stop"

Write-Warning "This project contains paid AWS resources including EKS, EC2 worker nodes, NAT Gateway and RDS/Aurora."
Write-Host "Destroying Kubernetes/Helm resources first..."
terraform destroy `
  -target=module.argo_cd `
  -target=module.monitoring `
  -target=module.jenkins `
  -auto-approve
if ($LASTEXITCODE -ne 0) { throw "Kubernetes/Helm destroy failed." }

Write-Host "Destroying database, EKS, ECR and VPC..."
terraform destroy `
  -target=module.rds `
  -target=module.eks `
  -target=module.ecr `
  -target=module.vpc `
  -auto-approve
if ($LASTEXITCODE -ne 0) { throw "AWS infrastructure destroy failed." }

Write-Warning "The S3 state bucket and DynamoDB lock table are intentionally left until last so Terraform does not lose its own backend during destruction."
Write-Host "After confirming the main infrastructure is gone, delete the backend resources manually only if you no longer need the state."
Write-Host "Bucket: $(terraform output -raw terraform_state_bucket)"
Write-Host "Table:  $(terraform output -raw terraform_lock_table)"
