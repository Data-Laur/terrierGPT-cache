FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy application code
COPY embedding_pipeline.py .
COPY cache_cli.py .

# Default command
ENTRYPOINT ["python", "cache_cli.py"]
CMD ["stats"]
