# Architecture

```text
Developer push to final-project branch
                |
                v
        Jenkins on Amazon EKS
        |       |          |
        |       |          +--> Django tests
        |       +-------------> Kaniko image build
        |                         |
        |                         v
        |                    Amazon ECR
        |
        +--> update charts/django-app/values.yaml
                         |
                         v
                      GitHub
                         |
                         v
                     Argo CD
                         |
                         v
                Helm deployment on EKS
                         |
              +----------+----------+
              |                     |
              v                     v
        Private RDS/Aurora      HPA / Metrics Server

Prometheus <--- cluster/workload metrics ---> Grafana
```

AWS network layout:

- One VPC across three Availability Zones by default.
- Public subnets host the NAT Gateway and can host public load balancers if enabled later.
- Private subnets host EKS worker nodes and the RDS/Aurora database.
- The database security group allows inbound database traffic only from the EKS worker-node security group.
- EKS has private API access enabled and configurable public API CIDR restrictions.
- Jenkins agents use IRSA and an ECR-scoped IAM policy instead of static AWS access keys.
