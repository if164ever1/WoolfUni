# Validation record

The project received the following local static and application checks before packaging:

- all Terraform `.tf` files parsed successfully as HCL;
- root module arguments were checked against the child-module variable declarations;
- root references to child-module outputs were checked against declared outputs;
- `templatefile()` placeholders were checked against the supplied template variable maps;
- all Terraform variables contain both `description` and `default`;
- all Terraform outputs contain `description`;
- all non-template YAML files parsed successfully;
- Python source compiled successfully;
- `DATABASE_ENGINE=sqlite python manage.py check` passed with no issues;
- the Django test suite passed: 2 tests;
- the repository was scanned for accidental absolute local paths and common secret patterns;
- the final ZIP archive integrity is checked after packaging.

The following checks require the real deployment environment and therefore were not claimed as executed here:

```bash
terraform fmt -recursive
terraform init -backend-config=backend.hcl -reconfigure
terraform validate
terraform plan
terraform apply
helm lint charts/django-app
kubectl get all -n jenkins
kubectl get all -n argocd
kubectl get all -n monitoring
```

The generation environment does not have the user's AWS credentials or an active EKS cluster, and its Terraform/Helm CLIs are not available for provider-aware validation. Run `scripts/apply.ps1` in the target environment, then run `scripts/verify.ps1` and capture the evidence listed in `README.md`.
