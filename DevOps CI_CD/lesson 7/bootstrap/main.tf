module "s3_backend" {
  source = "../modules/s3-backend"

  bucket_name = var.state_bucket_name
  table_name  = var.lock_table_name
}
