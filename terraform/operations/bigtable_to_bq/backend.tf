terraform {
  backend "gcs" {
    bucket = "adg-test-terraform-bucket"
    prefix = "adg-statefile"
  }
}