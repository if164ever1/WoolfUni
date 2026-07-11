# Lesson 7 — Terraform, Amazon EKS, ECR and Helm

This project creates an Amazon EKS cluster in the existing `lesson-5-vpc`,
creates an ECR repository, builds and uploads the Django image, and deploys
the application through a Helm chart with ConfigMap, LoadBalancer Service and HPA.

## Architecture

- Existing VPC and six subnets from lesson 5 are discovered by Terraform.
- Kubernetes discovery tags are added to the existing subnets.
- EKS control plane and a managed EC2 node group are created in private subnets.
- ECR stores the Django image.
- Helm deploys two Django replicas.
- A public AWS LoadBalancer exposes the application.
- HPA scales from 2 to 6 replicas when average CPU utilization exceeds 70%.
- Metrics Server supplies CPU metrics.
- ConfigMap is injected through `envFrom`.
- Sensitive values are stored in a Kubernetes Secret rather than ConfigMap.
- Optional Ingress and TLS settings are included but disabled by default.

## Prerequisites

Install and authenticate:

```powershell
aws --version
terraform version
docker --version
kubectl version --client
helm version
aws sts get-caller-identity
```

Use the same AWS account and region that contain the VPC from lesson 5.

> Important: the AWS account must have active access to S3, DynamoDB, EC2,
> IAM, EKS, ECR and Elastic Load Balancing. An account returning
> `NotSignedUp`, `SubscriptionRequiredException` or `OptInRequired` cannot
> create this infrastructure until AWS enables those services.

## Project structure

```text
lesson-7/
├── application/                 # Django application and Dockerfile
├── bootstrap/                   # Creates S3 backend and DynamoDB lock table
├── charts/django-app/           # Helm chart
├── modules/
│   ├── s3-backend/
│   ├── vpc/                     # Imports the existing lesson-5-vpc
│   ├── ecr/
│   └── eks/
├── scripts/                     # PowerShell automation
├── backend.tf
├── main.tf
├── outputs.tf
├── providers.tf
├── variables.tf
└── versions.tf
```

## 1. Verify the lesson 5 VPC

```powershell
aws ec2 describe-vpcs `
  --filters "Name=tag:Name,Values=lesson-5-vpc" `
  --query "Vpcs[].{VpcId:VpcId,Cidr:CidrBlock,State:State}" `
  --output table

aws ec2 describe-subnets `
  --filters "Name=tag:Name,Values=lesson-5-vpc-*" `
  --query "Subnets[].{Name:Tags[?Key=='Name']|[0].Value,SubnetId:SubnetId,AZ:AvailabilityZone,CIDR:CidrBlock}" `
  --output table
```

Terraform expects subnet Name tags matching:

- `lesson-5-vpc-public-*`
- `lesson-5-vpc-private-*`

## 2. Create the remote Terraform backend

Open `bootstrap/variables.tf` and set a globally unique S3 bucket name.

```powershell
cd bootstrap
terraform init
terraform fmt -recursive
terraform validate
terraform apply
```

Copy the `state_bucket_name` output into the `bucket` field in `../backend.tf`.

Return to the root directory:

```powershell
cd ..
terraform init -reconfigure
```

The backend must be bootstrapped separately because Terraform cannot store its
state in an S3 bucket before that bucket exists.

## 3. Configure variables

```powershell
Copy-Item terraform.tfvars.example terraform.tfvars
```

Review `terraform.tfvars`. The default region is `us-west-2`, matching lesson 5.

## 4. Create EKS and ECR

```powershell
terraform fmt -recursive
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
```

Useful outputs:

```powershell
terraform output
```

## 5. Configure kubectl

```powershell
aws eks update-kubeconfig `
  --region $(terraform output -raw aws_region) `
  --name $(terraform output -raw cluster_name)

kubectl get nodes
kubectl cluster-info
```

## 6. Build and upload the Django image to ECR

```powershell
$Region = terraform output -raw aws_region
$RepositoryUrl = terraform output -raw ecr_repository_url
$Registry = $RepositoryUrl.Split('/')[0]

aws ecr get-login-password --region $Region |
  docker login --username AWS --password-stdin $Registry

docker build -t lesson-7-django:latest .pplication
docker tag lesson-7-django:latest "$RepositoryUrl`:latest"
docker push "$RepositoryUrl`:latest"
```

Verify:

```powershell
aws ecr list-images `
  --repository-name lesson-7-django `
  --region $Region `
  --output table
```

## 7. Install Metrics Server

HPA cannot calculate CPU utilization without a metrics provider.

```powershell
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm repo update

helm upgrade --install metrics-server metrics-server/metrics-server `
  --namespace kube-system `
  --set args[0]=--kubelet-insecure-tls

kubectl get deployment metrics-server -n kube-system
kubectl top nodes
```

## 8. Validate and deploy the Helm chart

```powershell
$RepositoryUrl = terraform output -raw ecr_repository_url

helm lint .\charts\django-app
helm template django-app .\charts\django-app `
  --set "image.repository=$RepositoryUrl"

helm upgrade --install django-app .\charts\django-app `
  --namespace lesson-7 `
  --create-namespace `
  --set "image.repository=$RepositoryUrl" `
  --set "image.tag=latest"
```

## 9. Verify all acceptance criteria

```powershell
kubectl get deployments,pods,services,hpa,configmaps,secrets -n lesson-7
kubectl describe deployment django-app-django-app -n lesson-7
kubectl describe hpa django-app-django-app -n lesson-7
kubectl get service django-app-django-app -n lesson-7 --watch
```

When the Service receives an external hostname:

```powershell
$LoadBalancer = kubectl get service django-app-django-app `
  -n lesson-7 `
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

curl "http://$LoadBalancer/"
curl "http://$LoadBalancer/health/"
```

Expected response:

```json
{"status":"ok","application":"lesson-7-django","message":"Django is running in Amazon EKS."}
```

## 10. Test HPA

Create temporary CPU load:

```powershell
kubectl run load-generator `
  --image=busybox:1.36 `
  --restart=Never `
  -n lesson-7 `
  -- /bin/sh -c "while true; do wget -q -O- http://django-app-django-app; done"
```

Observe:

```powershell
kubectl get hpa -n lesson-7 --watch
kubectl get pods -n lesson-7 --watch
```

Delete the load generator:

```powershell
kubectl delete pod load-generator -n lesson-7
```

## ConfigMap and environment variables

The required non-sensitive settings are in `charts/django-app/values.yaml`
under `config` and are rendered into `templates/configmap.yaml`.

The Deployment imports them with:

```yaml
envFrom:
  - configMapRef:
      name: <release>-django-app-config
```

The original lesson 4 application expected PostgreSQL hostname `db`, which
exists only inside Docker Compose. This project defaults to SQLite so that the
Django workload can run without adding a database component outside the
assignment scope. Set `DATABASE_ENGINE: postgresql` only after providing a
reachable PostgreSQL service or managed database.

`DJANGO_SECRET_KEY` and `POSTGRES_PASSWORD` are intentionally placed in a
Secret template, because ConfigMap is not suitable for secrets.

## Bonus: Ingress and TLS

Edit `charts/django-app/values.yaml`:

```yaml
ingress:
  enabled: true
  className: nginx
  host: yourdomain.com
  path: /
  pathType: Prefix
  tls: true
  clusterIssuer: letsencrypt-prod
  secretName: django-app-tls
```

Before enabling it, install an ingress controller and cert-manager.

## GitHub submission

```powershell
git checkout -b lesson-7
git add .
git commit -m "Complete lesson 7 EKS ECR and Helm homework"
git push -u origin lesson-7
```

Submit:

1. Link to the `lesson-7` branch.
2. ZIP archive named `ДЗ7_Ігор_Задор.zip`.
3. A note stating whether you accept the first passing grade or intend to
   revise the work after mentor feedback.

## Cleanup

Delete Helm resources first, then Terraform infrastructure:

```powershell
helm uninstall django-app --namespace lesson-7
terraform destroy
```

The S3 state bucket and DynamoDB lock table have `prevent_destroy = true`.
Remove that protection only when you intentionally want to delete the backend.
