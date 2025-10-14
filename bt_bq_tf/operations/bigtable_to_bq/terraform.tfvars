project_id        = "gu1-top20-iacc"
region            = "europe-west1"
job_name          = "test-job"
container_spec_gcs_path = "gs://dataflow-templates-europe-west1/2025-10-01-00_RC00/flex/Bigtable_Change_Streams_to_BigQuery"
network="projects/gu1-top20-iacc/global/networks/dataflow-net"
subnetwork="regions/europe-west1/subnetworks/dataflow-subnet-euw"
parameters = {
  "bigQueryDataset" = "transaction_logs" 
  "bigtableReadInstanceId" = "transaction-logs"
  "bigtableReadTableId" = "transaction_log"
  "bigtableChangeStreamAppProfile" = "default"
  "bigQueryChangelogTablePartitionGranularity" = "DAY"
}