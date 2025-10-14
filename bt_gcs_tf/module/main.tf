terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.33.0"
    }
  }
}


resource "google_dataflow_job" "bigtable_to_gcs" {
  
  project               = var.project_id
  region                = var.region
  name                  = var.job_name
  template_gcs_path     = var.template_gcs_path
  temp_gcs_location     = var.temp_gcs_location
  network    = var.network        
  subnetwork = var.subnetwork  
  parameters            = var.parameters
  
}