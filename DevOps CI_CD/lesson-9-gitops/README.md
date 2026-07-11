# Lesson 8–9 GitOps repository

This repository is the desired-state repository watched by Argo CD.

Jenkins changes only these fields in `charts/django-app/values.yaml`:

- `image.repository`
- `image.tag`
- `config.IMAGE_TAG`

Argo CD automatically detects the commit, renders the Helm chart and synchronizes the Django application into the `django-app` namespace.

Do not build images from this repository. Application source and the Jenkinsfile belong in the separate CI repository.
