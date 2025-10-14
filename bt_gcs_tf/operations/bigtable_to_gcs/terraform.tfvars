project_id        = "gu1-top20-iacc"
region            = "europe-west1"
job_name          = "test-job"
template_gcs_path = "gs://dataflow-templates-europe-west1/latest/Cloud_Bigtable_to_GCS_Avro"
temp_gcs_location = "gs://dataflow-staging-europe-west1-971441253898/tmp/"
network="projects/gu1-top20-iacc/global/networks/dataflow-net"
subnetwork="regions/europe-west1/subnetworks/dataflow-subnet-euw"
parameters = {
  "bigtableProjectId" = "gu1-top20-iacc" 
  "bigtableInstanceId" = "transaction-logs"
  "bigtableTableId" = "event_log"
  "outputDirectory" = "gs://gcs-to-bq-batch/transaction_logs/test/"
  "filenamePrefix" = "test"
}