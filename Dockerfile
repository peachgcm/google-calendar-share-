FROM python:3.13-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port (will be overridden by cloud services)
EXPOSE 5001

# Run the application
CMD ["python", "app_simple.py"]
