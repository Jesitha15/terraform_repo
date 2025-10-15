project_id        = "gu1-top20-iacc"
region            = "europe-west1"
job_name          = "test-job"
container_spec_gcs_path = "gs://gcs-to-bq-batch/templates/bigtable_to_bq_flex.json"
network="projects/gu1-top20-iacc/global/networks/dataflow-net"
subnetwork="regions/europe-west1/subnetworks/dataflow-subnet-euw"
parameters = {
  "input_avro" = "gs://gcs-to-bq-batch/transaction_logs/avro_files/transaction_log_part-00000-of-00003.avro"
  "output_table" = "gu1-top20-iacc.transaction_logs.test"
  "source_instance" = "transaction-logs"
  "source_cluster" = "log-cluster"
  "source_table" = "event_log"
}