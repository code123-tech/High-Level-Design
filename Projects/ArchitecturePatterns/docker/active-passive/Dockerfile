FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app app/

# Set environment variables
ENV PYTHONPATH=/app
ENV MODULE_NAME=app.active_passive.main
ENV VARIABLE_NAME=app
ENV PORT=8000

# Run the application
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.active_passive.main:app"] 