$ErrorActionPreference = "Stop"

$region  = (& terraform output -raw aws_region).Trim()
$cluster = (& terraform output -raw cluster_name).Trim()

aws eks update-kubeconfig --region $region --name $cluster

Write-Host "=== EKS nodes ==="
kubectl get nodes -o wide

Write-Host "=== Jenkins ==="
kubectl get all -n jenkins

Write-Host "=== Argo CD ==="
kubectl get all -n argocd
kubectl get applications.argoproj.io -n argocd

Write-Host "=== Monitoring ==="
kubectl get all -n monitoring

Write-Host "=== Django application ==="
kubectl get deployment,pods,service,hpa,pdb,configmap,secret -n django-app

Write-Host "=== Metrics ==="
kubectl top nodes
kubectl get hpa -n django-app

Write-Host "=== Useful access commands ==="
terraform output -raw jenkins_port_forward_command
terraform output -raw argocd_port_forward_command
terraform output -raw grafana_port_forward_command
terraform output -raw prometheus_port_forward_command
