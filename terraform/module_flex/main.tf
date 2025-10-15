terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.33.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 6.33.0"
    }
  }
}


resource "google_dataflow_flex_template_job" "bigtable_to_bq" {
  provider               = google-beta
  project               = var.project_id
  region                = var.region
  name                  = var.job_name
  container_spec_gcs_path = var.container_spec_gcs_path
  network    = var.network        
  subnetwork = var.subnetwork  
  parameters            = var.parameters
  
}