FROM apache/beam_python3.9_sdk:2.51.0

WORKDIR /template
COPY testing.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="/template/testing.py"