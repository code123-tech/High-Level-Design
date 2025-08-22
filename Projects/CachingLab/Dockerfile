# Use full base instead of slim for broader compatibility
FROM python:3.10

# Upgrade pip first
RUN python -m pip install --upgrade pip

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
