# Use the official Dataflow base image
FROM gcr.io/dataflow-templates-base/python39-template-launcher-base

# Copy your code into the image
COPY . /dataflow/template/
WORKDIR /dataflow/template

# Install dependencies
RUN pip install --no-cache-dir apache-beam[gcp]==2.58.0

# Set environment variables
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="testing.py"

# Required entrypoint for Dataflow
ENTRYPOINT ["/opt/google/dataflow/python_template_launcher"]
