$ErrorActionPreference = "Stop"
Push-Location "$PSScriptRoot/.."
try {
  terraform destroy
}
finally {
  Pop-Location
}
