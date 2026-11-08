# Final DevOps Project — AWS, Terraform, EKS, Jenkins, Argo CD, RDS/Aurora, ECR, Prometheus and Grafana

This repository is the final integrated project built from the previous Terraform, Kubernetes, Helm, Jenkins, Argo CD and RDS/Aurora homework assignments.

The default architecture creates:

- an S3 bucket and DynamoDB lock table for Terraform state;
- a multi-AZ VPC with public/private subnets and NAT egress;
- an Amazon ECR repository;
- an Amazon EKS cluster with managed worker nodes, OIDC/IRSA and the EBS CSI add-on;
- a private PostgreSQL RDS database by default, or Aurora when `use_aurora = true`;
- Jenkins installed by Helm with Kubernetes agents and IRSA-based ECR push permissions;
- Argo CD installed by Helm and configured to continuously reconcile the Django Helm chart;
- Metrics Server for HPA metrics;
- Prometheus and Grafana through `kube-prometheus-stack`;
- a Django application deployed from `charts/django-app` with HPA from 2 to 6 replicas.

## 1. Clone the repository and switch to the final project branch

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
git checkout final-project
```

## 2. Install and verify prerequisites

Required tools:

```bash
terraform version
aws --version
kubectl version --client
helm version
git --version
aws sts get-caller-identity
```

The AWS account must have active access to S3, DynamoDB, VPC/EC2, IAM, EKS, ECR, RDS, Elastic Load Balancing and CloudWatch. If the account returns errors such as `NotSignedUp`, `SubscriptionRequiredException` or `OptInRequired`, AWS must enable those services before this project can be deployed.

## 3. Configure project variables

Create the local Terraform variables file:

Linux/macOS:

```bash
cp terraform.tfvars.example terraform.tfvars
```

PowerShell:

```powershell
Copy-Item terraform.tfvars.example terraform.tfvars
```

Edit at minimum:

- `state_bucket_name`: must be globally unique;
- `source_repository_url` (use an HTTPS Git URL);
- `source_project_path` (`.` at repository root, or the project subdirectory path in a monorepo);
- `jenkinsfile_path` (path from repository root);
- `gitops_repository_url` (use an HTTPS Git URL);
- GitOps branch and chart/value paths;
- `eks_public_access_cidrs`: preferably your current public IP with `/32` instead of `0.0.0.0/0`.

Create a fine-grained GitHub token with permission to read the repository and write repository Contents. Do not commit it.

PowerShell:

```powershell
$env:TF_VAR_github_token = "github_pat_REPLACE_WITH_REAL_TOKEN"
```

Bash:

```bash
export TF_VAR_github_token="github_pat_REPLACE_WITH_REAL_TOKEN"
```

Commit and push the `final-project` branch before Jenkins is installed because the Jenkins pipeline job reads `Django/Jenkinsfile` from Git.

## 4. Deploy the complete project

The first deployment has a bootstrap dependency: the S3 backend must exist before Terraform can use it, and EKS must exist before Kubernetes/Helm providers can install Jenkins, Argo CD and monitoring.

On Windows PowerShell, run the supplied deployment script from the project root:

```powershell
.\scripts\apply.ps1
```

The script performs these steps:

1. initializes Terraform with the backend temporarily disabled;
2. creates `module.s3_backend`;
3. generates `backend.hcl` and migrates state to S3;
4. creates VPC, ECR, EKS and RDS/Aurora;
5. configures `kubectl`;
6. runs the final full deployment with `terraform plan` and `terraform apply`.

After the first bootstrap, normal changes are deployed with:

```bash
terraform init -backend-config=backend.hcl -reconfigure
terraform plan -out=tfplan
terraform apply tfplan
```

## 5. Configure kubectl manually when needed

PowerShell:

```powershell
$Region = terraform output -raw aws_region
$Cluster = terraform output -raw cluster_name
aws eks update-kubeconfig --region $Region --name $Cluster
kubectl get nodes
```

Bash:

```bash
REGION=$(terraform output -raw aws_region)
CLUSTER=$(terraform output -raw cluster_name)
aws eks update-kubeconfig --region "$REGION" --name "$CLUSTER"
kubectl get nodes
```

## 6. Verify required namespaces and services

```bash
kubectl get all -n jenkins
kubectl get all -n argocd
kubectl get all -n monitoring
kubectl get deployment,pods,service,hpa,pdb -n django-app
```

On Windows, the complete check is automated:

```powershell
.\scripts\verify.ps1
```

## 7. Access Jenkins

```bash
kubectl port-forward svc/jenkins 8080:8080 -n jenkins
```

Open `http://localhost:8080`.

Credentials:

```bash
terraform output -raw jenkins_admin_username
terraform output -raw jenkins_admin_password
```

The `django-cicd` pipeline job is created by Jenkins Configuration as Code. The pipeline:

1. checks out the final project branch;
2. runs Django checks and tests;
3. builds the image with Kaniko inside an ephemeral Kubernetes agent;
4. pushes an immutable build tag to Amazon ECR using IRSA;
5. updates `charts/django-app/values.yaml` with the new image repository/tag;
6. pushes the GitOps change to Git;
7. lets Argo CD detect and deploy the new desired state.

The deployment commit contains `[skip ci]`. The Jenkinsfile detects that marker and skips build/deploy stages on the follow-up SCM poll, preventing a CI loop when the source and GitOps repository/branch are the same.

A successful Jenkins build proves the CI part of the project.

## 8. Access and verify Argo CD

```bash
kubectl port-forward svc/argocd-server 8081:443 -n argocd
```

Open `https://localhost:8081`.

Username:

```text
admin
```

Initial password on Linux/macOS:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 --decode
```

PowerShell:

```powershell
$Encoded = kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}'
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($Encoded))
```

Verify the GitOps application:

```bash
kubectl get applications.argoproj.io -n argocd
kubectl describe application django-app -n argocd
```

Expected state after a successful Jenkins build:

```text
Sync Status: Synced
Health Status: Healthy
```

## 9. Verify the Django deployment and autoscaling

```bash
kubectl get deployment,pods,service,hpa,pdb,configmap,secret -n django-app
kubectl rollout status deployment/django-app -n django-app
kubectl top nodes
kubectl get hpa -n django-app
```

Access Django locally:

```bash
kubectl port-forward svc/django-app 8000:80 -n django-app
```

Then open:

```text
http://localhost:8000/
http://localhost:8000/health/
```

The application receives database host/user configuration from Argo CD Helm parameters and the database password from a Kubernetes Secret created by Terraform. The RDS/Aurora security group accepts database traffic only from the EKS worker-node security group.

To demonstrate HPA scaling, generate temporary load:

```bash
kubectl run load-generator --image=busybox:1.36 --restart=Never -n django-app -- /bin/sh -c "while true; do wget -q -O- http://django-app/ >/dev/null; done"
kubectl get hpa -n django-app --watch
```

After the demonstration:

```bash
kubectl delete pod load-generator -n django-app
```

## 10. Access Grafana and Prometheus

Grafana:

```bash
kubectl port-forward svc/grafana 3000:80 -n monitoring
```

Open `http://localhost:3000`.

Credentials:

```bash
terraform output -raw grafana_admin_username
terraform output -raw grafana_admin_password
```

Prometheus:

```bash
kubectl port-forward svc/prometheus-operated 9090:9090 -n monitoring
```

Open `http://localhost:9090`.

In Grafana, open the preinstalled Kubernetes dashboards and verify node, pod, CPU and memory metrics. Metrics Server separately supplies resource metrics required by the Django HPA.

## 11. Switch from standard RDS to Aurora

Default PostgreSQL RDS:

```hcl
use_aurora                = false
db_engine                 = "postgres"
db_engine_version         = "16.3"
db_parameter_group_family = "postgres16"
db_instance_class         = "db.t3.micro"
```

Aurora requires an Aurora-compatible engine version, parameter family and supported instance class. Example values must be checked against the selected AWS region before applying:

```hcl
use_aurora                = true
db_engine                 = "postgres"
db_engine_version         = "16.3"
db_parameter_group_family = "aurora-postgresql16"
db_instance_class         = "db.r6g.large"
aurora_instance_count     = 1
```

Check regional database versions before switching:

```bash
aws rds describe-db-engine-versions --engine aurora-postgresql --query "DBEngineVersions[].EngineVersion" --output table
```

## 12. Evidence to capture for the mentor

Capture screenshots showing:

1. successful Terraform apply and outputs;
2. `kubectl get nodes` with Ready EKS nodes;
3. `kubectl get all -n jenkins`;
4. successful Jenkins `django-cicd` build stages;
5. the new immutable image tag in Amazon ECR;
6. the Git commit where Jenkins updated `charts/django-app/values.yaml`;
7. Argo CD application in `Synced` and `Healthy` state;
8. Django Deployment, Pods, Service and HPA;
9. `kubectl get all -n monitoring`;
10. Grafana dashboard with Kubernetes metrics.

## 13. Destroy paid infrastructure

Because the Terraform state itself is stored in S3, deleting the backend in the same operation that is still using it can corrupt or strand the final state. The included cleanup script therefore removes workloads first and leaves the backend until last:

```powershell
.\scripts\destroy.ps1
```

The script destroys Jenkins, Argo CD, monitoring, RDS/Aurora, EKS, ECR and VPC. After confirming those resources are gone, delete the S3 state bucket and DynamoDB lock table only when you no longer need the Terraform state.

Always verify the AWS console after cleanup, especially EKS, EC2 instances, NAT Gateways, Elastic IPs, RDS/Aurora and ECR.

## Security notes

- EKS worker nodes and the database run in private subnets.
- The database is not publicly accessible.
- The DB security group allows application traffic from the EKS worker-node security group rather than the public internet.
- Jenkins pushes to ECR through IRSA; no static AWS access keys are placed in the pipeline.
- ECR scanning and immutable tags are enabled.
- Terraform state is encrypted in S3, versioned and blocked from public access.
- GitHub and generated administrator credentials are sensitive and should not be committed. Terraform-managed secrets are present in Terraform state, so access to the S3 backend must be restricted.
- The default EKS public API allow-list is intentionally permissive for coursework convenience; replace it with your public `/32` CIDR.
