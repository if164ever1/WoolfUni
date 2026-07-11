SHELL := /bin/bash
TAG ?= latest
NAMESPACE ?= lesson-7

fmt:
	terraform fmt -recursive

validate:
	terraform init -backend=false
	terraform validate
	helm lint charts/django-app

plan:
	terraform plan -out=tfplan

apply:
	terraform apply tfplan

kubeconfig:
	aws eks update-kubeconfig --region $$(terraform output -raw aws_region) --name $$(terraform output -raw cluster_name)

build-push:
	REGION=$$(terraform output -raw aws_region); \
	REPO=$$(terraform output -raw ecr_repository_url); \
	REGISTRY=$${REPO%%/*}; \
	aws ecr get-login-password --region $$REGION | docker login --username AWS --password-stdin $$REGISTRY; \
	docker build -t lesson-7-django:$(TAG) application; \
	docker tag lesson-7-django:$(TAG) $$REPO:$(TAG); \
	docker push $$REPO:$(TAG)

deploy:
	helm upgrade --install django-app charts/django-app --namespace $(NAMESPACE) --create-namespace \
	  --set image.repository=$$(terraform output -raw ecr_repository_url) \
	  --set image.tag=$(TAG)

destroy:
	helm uninstall django-app --namespace $(NAMESPACE) || true
	terraform destroy
