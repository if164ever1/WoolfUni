$ErrorActionPreference = "Stop"

Push-Location "$PSScriptRoot/../bootstrap"
try {
  if (-not (Test-Path "terraform.tfvars")) {
    Copy-Item "terraform.tfvars.example" "terraform.tfvars"
    throw "Edit bootstrap/terraform.tfvars and set a globally unique S3 bucket name, then rerun this script."
  }

  terraform init
  terraform fmt -recursive
  terraform validate
  terraform apply

  Write-Host "Backend created. Copy the output values into ../backend.tf, then run scripts/apply.ps1."
}
finally {
  Pop-Location
}
