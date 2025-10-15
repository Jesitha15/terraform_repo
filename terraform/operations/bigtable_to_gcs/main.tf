module "bt_to_gcs" {
  source = "../../module_classic"
  
  project_id            = var.project_id
  region                = var.region
  job_name              = var.job_name
  template_gcs_path     = var.template_gcs_path
  temp_gcs_location     = var.temp_gcs_location
  network    = var.network        
  subnetwork = var.subnetwork  
  parameters            = var.parameters
}