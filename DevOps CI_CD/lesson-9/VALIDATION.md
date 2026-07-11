# Validation record

The generated project received the following local, non-cloud checks:

- Parsed all Terraform `.tf` files as HCL: passed.
- Parsed all non-template YAML files: passed.
- Compared the submission Helm chart and separate GitOps Helm chart byte-for-byte: passed.
- Compiled the Django Python source: passed.
- Executed `python manage.py check`: passed with no issues.
- Executed the Django test suite: 2 tests passed.
- Tested ZIP archive integrity: passed.

Cloud-dependent checks were not executed in the generation environment:

- `terraform init/plan/apply` against the user's AWS account.
- Helm installation into the user's EKS cluster.
- Jenkins agent execution, ECR push, GitHub push, and Argo CD reconciliation.

Those checks require active AWS services, valid AWS credentials, a real GitHub token, and the two GitHub repositories described in `README.md`.
