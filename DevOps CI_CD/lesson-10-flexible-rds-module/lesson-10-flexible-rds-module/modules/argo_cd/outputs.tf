output "release_name" {
  description = "Name of the Argo CD Helm release."
  value       = helm_release.this.name
}

output "namespace" {
  description = "Namespace containing Argo CD."
  value       = helm_release.this.namespace
}
