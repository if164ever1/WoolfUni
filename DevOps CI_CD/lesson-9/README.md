# Lesson 9 — Jenkins, Kaniko, ECR, Helm, Terraform and Argo CD

This project implements a complete CI/CD chain for a Django application:

1. Terraform discovers the existing `lesson-5-vpc` and creates ECR and EKS.
2. Terraform installs Metrics Server and Jenkins with Helm.
3. Jenkins creates ephemeral Kubernetes agents containing Python, Git, Kaniko and `yq` containers.
4. Kaniko builds the Django image without a Docker daemon and pushes an immutable tag to ECR using IRSA.
5. Jenkins updates the image repository/tag in a separate GitOps repository and pushes to `main`.
6. Terraform installs Argo CD with the official Helm chart.
7. Argo CD watches the GitOps Helm chart and automatically synchronizes, prunes and self-heals the Django workload.

## Architecture

```text
Developer push
      |
      v
Jenkins controller (EKS)
      |
      v
Ephemeral Kubernetes agent
  | Kaniko -> Amazon ECR
  | Git/yq -> GitOps repository main
                    |
                    v
               Argo CD
                    |
                    v
           Helm -> Django on EKS
```

The Mermaid source is in `docs/architecture.mmd`.

## Repository separation

The delivery archive contains two repositories:

- `application-repo`: this directory.
- `gitops-repo`: sibling directory containing the chart watched by Argo CD.


## Project structure

```text
application-repo/
├── application/                  # Django source and Dockerfile
├── bootstrap/                    # One-time S3/DynamoDB backend creation
├── charts/django-app/            # Submission copy of the GitOps chart
├── docs/
├── modules/
│   ├── s3-backend/
│   ├── vpc/                      # Discovers lesson-5-vpc and tags subnets
│   ├── ecr/
│   ├── eks/                      # EKS, managed nodes, OIDC and EBS CSI
│   ├── jenkins/                  # Helm, JCasC, IRSA and seeded pipeline job
│   └── argo_cd/                  # Helm and declarative Application chart
├── scripts/
├── backend.tf
├── Jenkinsfile
├── main.tf
├── metrics-server.tf             # Metrics API required by HPA
├── outputs.tf
├── providers.tf
├── terraform.tfvars.example
├── variables.tf
└── versions.tf
```

## Prerequisites

Install and authenticate:

```powershell
aws --version
terraform version
kubectl version --client
helm version
git --version
aws sts get-caller-identity
```

The AWS account must have active access to S3, DynamoDB, EC2, IAM, ECR, EKS and Elastic Load Balancing. An account returning `NotSignedUp`, `SubscriptionRequiredException` or `OptInRequired` cannot apply this project until AWS enables those services.

The existing VPC must contain at least two subnets whose Name tags match:

```text
lesson-5-vpc-public-*
lesson-5-vpc-private-*
```

Verify:

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

## 0. Publish the source branch before Terraform

Jenkins is configured from Git and automatically queues its first build. Therefore, the `lesson-8-9` branch and Jenkinsfile must already exist before Jenkins is installed.

Copy the contents of `application-repo/` into:

```text
WoolfUni/DevOps CI_CD/lesson-9/
```

Then, from the `WoolfUni` repository root:

```powershell
git checkout -b lesson-9
git add "DevOps CI_CD/lesson-9"
git commit -m "Add lesson 8-9 Jenkins and Argo CD CI/CD project"
git push -u origin lesson-8-9
```

## 1. Create the separate GitOps repository

Create a GitHub repository named `lesson-9-gitops`, then copy the sibling `gitops-repo/` contents into it and push `main`:

```powershell
cd ..\gitops-repo
git init
git add .
git commit -m "Initialize lesson 9 GitOps chart"
git branch -M main
git remote add origin https://github.com/if164ever1/lesson-9-gitops.git
git push -u origin main
```

## 2. Create a GitHub token

Use a fine-grained GitHub personal access token with:

- Read access to the source repository.
- Read and write `Contents` access to `lesson-9-gitops`.

Do not write the token into committed files. In PowerShell:

```powershell
$env:TF_VAR_github_token = "github_pat_REPLACE_WITH_REAL_TOKEN"
```

Terraform places the token into Kubernetes Secrets for Jenkins and Argo CD. It is marked sensitive in Terraform output, but, like any Terraform-managed secret, it is present in encrypted Terraform state. Restrict access to the S3 backend.

## 3. Bootstrap S3 and DynamoDB

```powershell
cd bootstrap
Copy-Item terraform.tfvars.example terraform.tfvars
```

Edit `bootstrap/terraform.tfvars` and choose a globally unique bucket name. Then:

```powershell
terraform init
terraform fmt -recursive
terraform validate
terraform apply
terraform output
```

Copy the bucket/table names into the root `backend.tf`, then return:

```powershell
cd ..
```

## 4. Configure Terraform variables

```powershell
Copy-Item terraform.tfvars.example terraform.tfvars
```

Review:

- AWS region.
- Source repository URL/branch/Jenkinsfile path.
- Separate GitOps repository URL.
- EKS endpoint allow-list.
- Jenkins and Argo CD Service types.

The default chart pins are:

- Jenkins chart `5.9.33`.
- Argo CD chart `10.1.3`.
- Metrics Server chart `3.13.1`.
- EKS Kubernetes `1.36`.

## 5. Apply Terraform

Because the Kubernetes and Helm providers cannot connect until EKS exists, use the supplied two-phase script:

```powershell
.\scripts\apply.ps1
```

Equivalent manual sequence:

```powershell
terraform init -reconfigure
terraform fmt -recursive
terraform validate
terraform apply `
  -target=module.vpc `
  -target=module.ecr `
  -target=module.eks `
  -auto-approve

$Region = terraform output -raw aws_region
$Cluster = terraform output -raw cluster_name
aws eks update-kubeconfig --region $Region --name $Cluster
kubectl get nodes

terraform plan -out tfplan
terraform apply tfplan
kubectl get pods --all-namespaces
```

## 6. Access Jenkins

For the default `ClusterIP` service:

```powershell
kubectl port-forward service/jenkins 8080:8080 --namespace jenkins
```

Open `http://localhost:8080`.

Credentials:

```powershell
terraform output -raw jenkins_admin_username
terraform output -raw jenkins_admin_password
```

Terraform/JCasC automatically creates and queues the first `django-cicd` build, then polls the source branch every five minutes. The Jenkinsfile detects whether it runs from this directory as a standalone repository or from `DevOps CI_CD/lesson-9/` inside `WoolfUni`.

Check the agent and controller:

```powershell
kubectl get pods -n jenkins -w
kubectl logs -n jenkins statefulset/jenkins -c jenkins
kubectl get serviceaccount jenkins-agent -n jenkins -o yaml
```

The agent service account is annotated with an IAM role that grants only ECR authorization and push/pull permissions for the project repository.

## 7. Verify the Jenkins pipeline

A successful run has these stages. The first run is queued automatically so that the initial placeholder image in the GitOps chart is replaced without manual deployment commands:

1. Checkout source.
2. Install dependencies and run `manage.py check` plus Django tests.
3. Build and push the image with Kaniko.
4. Clone the GitOps repository.
5. Update Helm `image.repository`, `image.tag` and `config.IMAGE_TAG` with `yq`.
6. Commit and push the desired state to `main`.

Verify ECR:

```powershell
aws ecr list-images `
  --repository-name lesson-9-django `
  --region us-west-2 `
  --output table
```

Verify the GitOps commit:

```powershell
git -C ..\gitops-repo pull
Get-Content ..\gitops-repo\charts\django-app\values.yaml
```

## 8. Access and verify Argo CD

For the default `ClusterIP` service:

```powershell
kubectl port-forward service/argo-cd-argocd-server 8081:80 --namespace argocd
```

Open `http://localhost:8081`.

Username: `admin`

Password:

```powershell
terraform output -raw argocd_admin_password
```

Verify the Application:

```powershell
kubectl get applications.argoproj.io -n argocd
kubectl describe application django-app -n argocd
```

Expected status:

```text
Sync Status: Synced
Health Status: Healthy
```

## 9. Verify the deployed Django application

```powershell
kubectl get deployment,pods,service,hpa,pdb,configmap -n django-app
kubectl rollout status deployment/django-app -n django-app
kubectl get deployment metrics-server -n kube-system
kubectl top nodes
kubectl get hpa -n django-app
```

Wait for the public hostname:

```powershell
kubectl get service django-app -n django-app --watch
```

Then:

```powershell
$LoadBalancer = kubectl get service django-app `
  -n django-app `
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

curl "http://$LoadBalancer/"
curl "http://$LoadBalancer/health/"
```

Expected response includes the Jenkins image tag:

```json
{
  "status": "ok",
  "application": "lesson-8-9-django",
  "message": "Django was deployed by Jenkins, ECR, Helm and Argo CD.",
  "image_tag": "<jenkins-build>-<git-sha>"
}
```

## 10. Prove automatic CD

Change a Django response, commit and push the source branch. Jenkins will:

- generate a new immutable tag;
- push it to ECR;
- update the GitOps repository.

Argo CD will then deploy the new tag without a manual `helm upgrade` or `kubectl apply`.

Observe:

```powershell
kubectl get application django-app -n argocd --watch
kubectl rollout status deployment/django-app -n django-app
kubectl get pods -n django-app -w
```

## Security and design notes

- Jenkins agents are ephemeral Kubernetes Pods.
- Kaniko does not require privileged Docker-in-Docker.
- ECR access uses IRSA; no static AWS access key is injected into Jenkins.
- ECR tags are immutable.
- GitHub credentials are stored in Kubernetes Secrets and consumed through JCasC/credentials binding.
- Argo CD uses automated sync, prune, self-heal and namespace creation.
- The EKS endpoint defaults to `0.0.0.0/0` only for coursework convenience. Restrict it to your public `/32` CIDR.
- `ClusterIP` is the default for Jenkins and Argo CD to avoid two additional public load balancers. The Django service remains `LoadBalancer` because the assignment requires a visible application result.

## Known external prerequisite

The code can be validated without AWS, but it cannot create cloud resources while the AWS account reports service-subscription errors. Resolve AWS account activation first.
