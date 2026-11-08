output "release_name" {
  description = "Name of the Jenkins Helm release."
  value       = helm_release.this.name
}

output "namespace" {
  description = "Namespace containing Jenkins."
  value       = helm_release.this.namespace
}
