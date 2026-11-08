$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\bootstrap"
terraform init
terraform fmt -recursive
terraform validate
terraform apply
