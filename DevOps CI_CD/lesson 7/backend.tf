# The S3 bucket and DynamoDB table must exist before this backend can be initialized.
# Create them first:
#   cd bootstrap
#   terraform init
#   terraform apply
#
# Then replace the placeholder bucket name below with the output from bootstrap
# and run:
#   terraform init -reconfigure

terraform {
  backend "s3" {
    bucket         = "REPLACE_WITH_UNIQUE_STATE_BUCKET_NAME"
    key            = "lesson-7/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "lesson-7-terraform-locks"
    encrypt        = true
  }
}
