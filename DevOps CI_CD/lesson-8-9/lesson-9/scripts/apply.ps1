$ErrorActionPreference = "Stop"
Push-Location "$PSScriptRoot/.."
try {
  if (-not (Test-Path "terraform.tfvars")) {
    Copy-Item "terraform.tfvars.example" "terraform.tfvars"
    throw "Review terraform.tfvars and export TF_VAR_github_token before applying."
  }

  if (-not $env:TF_VAR_github_token) {
    throw 'Set $env:TF_VAR_github_token = "github_pat_..." before applying.'
  }

  terraform init -reconfigure
  terraform fmt -recursive
  terraform validate

  # Phase 1: AWS resources must exist before Kubernetes and Helm providers connect.
  terraform apply `
    -target=module.vpc `
    -target=module.ecr `
    -target=module.eks `
    -auto-approve

  $Region = terraform output -raw aws_region
  $Cluster = terraform output -raw cluster_name
  aws eks update-kubeconfig --region $Region --name $Cluster
  kubectl get nodes

  # Phase 2: install Metrics Server, Jenkins, and Argo CD into the live cluster.
  terraform plan -out tfplan
  terraform apply tfplan

  kubectl get pods --all-namespaces
  terraform output
}
finally {
  Pop-Location
}
