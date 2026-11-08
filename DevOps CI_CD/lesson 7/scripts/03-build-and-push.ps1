param(
    [string]$Tag = "latest"
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
Set-Location $Root

$Region = terraform output -raw aws_region 2>$null
if (-not $Region) { $Region = "us-west-2" }

$RepositoryUrl = terraform output -raw ecr_repository_url
$Registry = $RepositoryUrl.Split('/')[0]

aws ecr get-login-password --region $Region |
    docker login --username AWS --password-stdin $Registry

docker build -t "lesson-7-django:$Tag" "$Root\application"
docker tag "lesson-7-django:$Tag" "$RepositoryUrl`:$Tag"
docker push "$RepositoryUrl`:$Tag"

Write-Host "Pushed image: $RepositoryUrl`:$Tag"
