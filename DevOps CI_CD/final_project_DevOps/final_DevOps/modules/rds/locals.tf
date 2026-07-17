locals {
  aurora_engine = var.engine == "postgres" ? "aurora-postgresql" : "aurora-mysql"
  db_port       = var.engine == "postgres" ? 5432 : 3306

  generated_password = var.manage_master_user_password ? null : (
    var.master_password != null ? var.master_password : random_password.master[0].result
  )
}
