$ErrorActionPreference = "Stop"
Push-Location "$PSScriptRoot/.."
try {
  terraform fmt -recursive
  terraform init -backend=false
  terraform validate

  if (Get-Command helm -ErrorAction SilentlyContinue) {
    helm lint "$PSScriptRoot/../../gitops-repo/charts/django-app"
    helm lint "$PSScriptRoot/../modules/argo_cd/charts/argocd-apps"
  }

  if (Get-Command python -ErrorAction SilentlyContinue) {
    Push-Location application
    try {
      python -m compileall .
    }
    finally {
      Pop-Location
    }
  }
}
finally {
  Pop-Location
}
