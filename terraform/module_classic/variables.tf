variable "project_id" {
  description = "The GCP project ID where the Dataflow job runs."
  type        = string
}

variable "region" {
  description = "The region where the Dataflow job will run."
  type        = string
  default     = "us-central1"
}

variable "job_name" {
  description = "Name for the Dataflow job."
  type        = string
}

variable "template_gcs_path" {
  description = "GCS path for Dataflow pre-built template job path."
  type        = string
}

variable "temp_gcs_location" {
  description = "GCS path for temporary Dataflow files (e.g., gs://bucket/temp/)."
  type        = string
}

variable "parameters" {
  description = "Dataflow job template parameters"
  type        = map(string)
}

variable "network" {
  type        = string
  description = "GCP network for Dataflow workers"
}

variable "subnetwork" {
  type        = string
  description = "GCP subnetwork for Dataflow workers"
}