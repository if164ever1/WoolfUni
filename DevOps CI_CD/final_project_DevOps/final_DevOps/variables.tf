variable "project_name" {
  description = "Short project name used in AWS resource names and tags."
  type        = string
  default     = "final-devops"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region used for all regional resources."
  type        = string
  default     = "us-west-2"
}

variable "additional_tags" {
  description = "Additional tags merged with the project-wide default tags."
  type        = map(string)
  default     = {}
}

variable "state_bucket_name" {
  description = "Globally unique S3 bucket name used for Terraform remote state."
  type        = string
  default     = "replace-with-globally-unique-final-devops-state-bucket"
}

variable "state_lock_table_name" {
  description = "DynamoDB table used for Terraform state locking."
  type        = string
  default     = "terraform-locks"
}

variable "vpc_cidr" {
  description = "CIDR block for the project VPC."
  type        = string
  default     = "10.40.0.0/16"
}

variable "availability_zone_count" {
  description = "Number of availability zones used for public and private subnets."
  type        = number
  default     = 3
}

variable "enable_nat_gateway" {
  description = "Whether private subnets receive outbound internet access through NAT."
  type        = bool
  default     = true
}

variable "single_nat_gateway" {
  description = "Use one NAT Gateway for all private subnets to reduce coursework cost."
  type        = bool
  default     = true
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository that stores Django application images."
  type        = string
  default     = "final-devops-django"
}

variable "ecr_force_delete" {
  description = "Allow Terraform to delete the ECR repository even when Jenkins has pushed images."
  type        = bool
  default     = true
}

variable "ecr_image_retention_count" {
  description = "Number of recent ECR images retained by the lifecycle policy."
  type        = number
  default     = 30
}

variable "eks_cluster_name" {
  description = "Name of the Amazon EKS cluster."
  type        = string
  default     = "final-devops-eks"
}

variable "eks_kubernetes_version" {
  description = "Kubernetes version used by the EKS control plane."
  type        = string
  default     = "1.36"
}

variable "eks_cluster_log_retention_days" {
  description = "Retention period in days for EKS control-plane logs in CloudWatch."
  type        = number
  default     = 7
}

variable "eks_public_access_cidrs" {
  description = "CIDR blocks allowed to reach the public EKS API endpoint. Replace 0.0.0.0/0 with your public /32 for real use."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "eks_node_instance_types" {
  description = "EC2 instance types used by the EKS managed node group."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "eks_node_capacity_type" {
  description = "EKS node group capacity type: ON_DEMAND or SPOT."
  type        = string
  default     = "ON_DEMAND"
}

variable "eks_node_desired_size" {
  description = "Desired EKS worker node count."
  type        = number
  default     = 2
}

variable "eks_node_min_size" {
  description = "Minimum EKS worker node count."
  type        = number
  default     = 2
}

variable "eks_node_max_size" {
  description = "Maximum EKS worker node count."
  type        = number
  default     = 4
}

variable "eks_node_disk_size" {
  description = "Root volume size in GiB for EKS worker nodes."
  type        = number
  default     = 30
}

variable "use_aurora" {
  description = "When true, create an Aurora cluster; otherwise create one standard RDS instance."
  type        = bool
  default     = false
}

variable "db_engine" {
  description = "Logical database engine: postgres or mysql."
  type        = string
  default     = "postgres"
}

variable "db_engine_version" {
  description = "Database engine version available in the selected AWS region."
  type        = string
  default     = "16.3"
}

variable "db_parameter_group_family" {
  description = "Parameter group family matching the selected database engine/version."
  type        = string
  default     = "postgres16"
}

variable "db_instance_class" {
  description = "RDS or Aurora instance class."
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Initial application database name."
  type        = string
  default     = "appdb"
}

variable "db_username" {
  description = "Master database username."
  type        = string
  default     = "dbadmin"
}

variable "db_password" {
  description = "Optional explicit database password. When null and AWS-managed password is disabled, the module generates one."
  type        = string
  default     = null
  sensitive   = true
}

variable "db_manage_master_user_password" {
  description = "Let AWS Secrets Manager manage the master password. Keep false when the Django demo should receive the generated password as a Kubernetes Secret."
  type        = bool
  default     = false
}

variable "db_multi_az" {
  description = "Enable Multi-AZ for standard RDS. Ignored for Aurora."
  type        = bool
  default     = false
}

variable "aurora_instance_count" {
  description = "Number of Aurora cluster instances when use_aurora is true."
  type        = number
  default     = 1
}

variable "db_allocated_storage" {
  description = "Initial storage size in GiB for standard RDS."
  type        = number
  default     = 20
}

variable "db_max_allocated_storage" {
  description = "Maximum autoscaled storage size in GiB for standard RDS."
  type        = number
  default     = 100
}

variable "db_backup_retention_period" {
  description = "Automated database backup retention in days."
  type        = number
  default     = 7
}

variable "db_deletion_protection" {
  description = "Protect the database from accidental deletion. Disabled by default for coursework cleanup."
  type        = bool
  default     = false
}

variable "db_skip_final_snapshot" {
  description = "Skip the final DB snapshot when destroying disposable coursework infrastructure."
  type        = bool
  default     = true
}

variable "db_custom_parameters" {
  description = "Additional engine-compatible DB parameters."
  type        = map(string)
  default     = {}
}

variable "source_project_path" {
  description = "Path from the source repository root to this final project. Use . when the project is at repository root."
  type        = string
  default     = "."
}

variable "source_repository_url" {
  description = "Git repository containing this final project and Django/Jenkinsfile."
  type        = string
  default     = "https://github.com/REPLACE_ME/REPLACE_ME.git"
}

variable "source_repository_branch" {
  description = "Git branch Jenkins checks out."
  type        = string
  default     = "final-project"
}

variable "jenkinsfile_path" {
  description = "Path to the pipeline Jenkinsfile inside the source repository."
  type        = string
  default     = "Django/Jenkinsfile"
}

variable "gitops_repository_url" {
  description = "Repository watched by Argo CD and updated by Jenkins. It may be the same repository as source_repository_url."
  type        = string
  default     = "https://github.com/REPLACE_ME/REPLACE_ME.git"
}

variable "gitops_repository_branch" {
  description = "Git branch watched by Argo CD and updated by Jenkins."
  type        = string
  default     = "final-project"
}

variable "gitops_chart_path" {
  description = "Path to the Django Helm chart inside the GitOps repository."
  type        = string
  default     = "charts/django-app"
}

variable "gitops_values_path" {
  description = "Path Jenkins edits after pushing a new ECR image."
  type        = string
  default     = "charts/django-app/values.yaml"
}

variable "github_username" {
  description = "GitHub username stored in the Jenkins credential used for authenticated pushes."
  type        = string
  default     = "git"
}

variable "github_token" {
  description = "Fine-grained GitHub token used by Jenkins to push GitOps updates. Prefer TF_VAR_github_token rather than terraform.tfvars."
  type        = string
  default     = ""
  sensitive   = true
}

variable "jenkins_namespace" {
  description = "Kubernetes namespace for Jenkins."
  type        = string
  default     = "jenkins"
}

variable "jenkins_chart_version" {
  description = "Pinned Jenkins Helm chart version."
  type        = string
  default     = "5.9.33"
}

variable "argocd_namespace" {
  description = "Kubernetes namespace for Argo CD."
  type        = string
  default     = "argocd"
}

variable "argocd_chart_version" {
  description = "Pinned Argo CD Helm chart version."
  type        = string
  default     = "10.1.3"
}

variable "monitoring_namespace" {
  description = "Kubernetes namespace for Prometheus and Grafana."
  type        = string
  default     = "monitoring"
}

variable "kube_prometheus_stack_chart_version" {
  description = "Pinned kube-prometheus-stack Helm chart version."
  type        = string
  default     = "86.0.1"
}

variable "metrics_server_chart_version" {
  description = "Pinned Metrics Server Helm chart version used by the Django HPA."
  type        = string
  default     = "3.13.1"
}
