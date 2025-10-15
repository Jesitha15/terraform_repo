module "gcs_to_bq" {
  source = "../module"
  
  project_id            = var.project_id
  region                = var.region
  job_name              = var.job_name
  container_spec_gcs_path     = var.container_spec_gcs_path
  network    = var.network        
  subnetwork = var.subnetwork  
  parameters            = var.parameters
}