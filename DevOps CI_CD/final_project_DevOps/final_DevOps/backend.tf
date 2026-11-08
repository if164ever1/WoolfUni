terraform {
  # The concrete bucket/table values are supplied from backend.hcl.
  # This allows the same repository to bootstrap the S3 + DynamoDB backend first.
  backend "s3" {}
}
