$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\.."
terraform init -reconfigure
terraform fmt -recursive
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
