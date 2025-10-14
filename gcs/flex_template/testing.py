import json
import apache_beam as beam
from apache_beam.options.pipeline_options import (
    PipelineOptions,
    GoogleCloudOptions,
    StandardOptions,
    SetupOptions,
)
from apache_beam.io import avroio
from datetime import datetime, timezone


class TransformToBigQuery(beam.DoFn):
    def __init__(self, source_instance, source_cluster, source_table):
        self.source_instance = source_instance
        self.source_cluster = source_cluster
        self.source_table = source_table

    def process(self, record):
        source_instance = self.source_instance.get()
        source_cluster = self.source_cluster.get()
        source_table = self.source_table.get()

        row_key = record.get("key")
        if isinstance(row_key, (bytes, bytearray)):
            row_key = row_key.decode("utf-8")

        cells = record.get("cells", [])
        if not cells:
            return

        ts = datetime.now(timezone.utc).isoformat()

        for cell in cells:
            try:
                value = (
                    [cell["value"].decode("utf-8")]
                    if isinstance(cell["value"], (bytes, bytearray))
                    else [cell["value"]]
                    if not isinstance(cell["value"], list)
                    else cell["value"]
                )

                if value and isinstance(value, list) and value[0]:
                    try:
                        parsed_data = json.loads(value[0])
                    except Exception:
                        parsed_data = str(value[0])

                    if isinstance(parsed_data, dict):
                        parsed_data = parsed_data
                    else:
                        qualifier = cell.get("qualifier", "value")
                        if isinstance(qualifier, (bytes, bytearray)):
                            qualifier = qualifier.decode("utf-8")
                        parsed_data = {qualifier: parsed_data}
                else:
                    parsed_data = {}
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                parsed_data = {}

            for json_key, json_val in parsed_data.items():
                yield {
                    "row_key": row_key or "UNKNOWN_KEY",
                    "mod_type": "SET_CELL_BATCH",
                    "commit_timestamp": ts,
                    "column_family": (
                        cell.get("family").decode("utf-8")
                        if isinstance(cell.get("family"), (bytes, bytearray))
                        else str(cell.get("family"))
                    ),
                    "column": json_key,
                    "timestamp": (
                        datetime.fromtimestamp(cell.get("timestamp") / 1e6, tz=timezone.utc).isoformat()
                        if cell.get("timestamp")
                        else None
                    ),
                    "value": str(json_val) if json_val is not None else None,
                    "timestamp_from": None,
                    "timestamp_to": None,
                    "is_gc": False,
                    "source_instance": source_instance,
                    "source_cluster": source_cluster,
                    "source_table": source_table,
                    "tiebreaker": 0,
                    "big_query_commit_timestamp": ts,
                }


class SelectLatestTimestampByColumn(beam.DoFn):
    def process(self, element):
        (row_key, column), records = element
        if not records:
            return
        latest_record = max(
            records,
            key=lambda x: x["timestamp"] if x["timestamp"] else "1970-01-01T00:00:00+00:00"
        )
        yield latest_record


class TemplateOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument("--source_instance", help="Source Bigtable instance")
        parser.add_value_provider_argument("--source_cluster", help="Source Bigtable cluster")
        parser.add_value_provider_argument("--source_table", help="Source Bigtable table")
        parser.add_value_provider_argument("--input_avro", help="Input Avro GCS path")
        parser.add_value_provider_argument("--output_table", help="Output BigQuery table")

def run(argv=None):
    pipeline_options = PipelineOptions(argv)
    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    standard_options = pipeline_options.view_as(StandardOptions)

    # DataflowRunner for Flex Template
    standard_options.runner = "DataflowRunner"
    pipeline_options.view_as(SetupOptions).save_main_session = True

    template_options = pipeline_options.view_as(TemplateOptions)

    # ---- BigQuery Schema ----
    table_schema = {
        "fields": [
            {"name": "row_key", "type": "STRING", "mode": "REQUIRED"},
            {"name": "mod_type", "type": "STRING", "mode": "REQUIRED"},
            {"name": "commit_timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
            {"name": "column_family", "type": "STRING", "mode": "REQUIRED"},
            {"name": "column", "type": "STRING", "mode": "REQUIRED"},
            {"name": "timestamp", "type": "TIMESTAMP"},
            {"name": "value", "type": "STRING"},
            {"name": "timestamp_from", "type": "TIMESTAMP"},
            {"name": "timestamp_to", "type": "TIMESTAMP"},
            {"name": "is_gc", "type": "BOOL", "mode": "REQUIRED"},
            {"name": "source_instance", "type": "STRING", "mode": "REQUIRED"},
            {"name": "source_cluster", "type": "STRING", "mode": "REQUIRED"},
            {"name": "source_table", "type": "STRING", "mode": "REQUIRED"},
            {"name": "tiebreaker", "type": "INT64", "mode": "REQUIRED"},
            {"name": "big_query_commit_timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
        ]
    }

    # ---- Pipeline Steps ----
    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | "Read Avro" >> avroio.ReadFromAvro(template_options.input_avro)
            | "Transform Records" >> beam.ParDo(
                TransformToBigQuery(
                    template_options.source_instance,
                    template_options.source_cluster,
                    template_options.source_table,
                )
            )
            | "Group by Row Key and Column" >> beam.GroupBy(lambda x: (x["row_key"], x["column"]))
            | "Select Latest Timestamp" >> beam.ParDo(SelectLatestTimestampByColumn())
            | "Write to BQ" >> beam.io.WriteToBigQuery(
                table=template_options.output_table,
                schema=table_schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )


if __name__ == "__main__":
    run()
