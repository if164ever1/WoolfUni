$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
Set-Location $Root

helm uninstall django-app --namespace lesson-7 2>$null
terraform destroy
