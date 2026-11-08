param(
    [string]$Tag = "latest",
    [string]$Namespace = "lesson-7"
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
Set-Location $Root

$Region = terraform output -raw aws_region
$ClusterName = terraform output -raw cluster_name
$RepositoryUrl = terraform output -raw ecr_repository_url

aws eks update-kubeconfig --region $Region --name $ClusterName

helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm repo update
helm upgrade --install metrics-server metrics-server/metrics-server `
  --namespace kube-system `
  --set args[0]=--kubelet-insecure-tls

helm lint "$Root\charts\django-app"
helm upgrade --install django-app "$Root\charts\django-app" `
  --namespace $Namespace `
  --create-namespace `
  --set "image.repository=$RepositoryUrl" `
  --set "image.tag=$Tag"

kubectl get pods,service,hpa,configmap -n $Namespace
