FROM python:3.11-slim

WORKDIR /app

# Install Flask
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app
COPY index.py .

# Expose port
EXPOSE 5000

# Start the Flask server
CMD ["python3", "index.py"]
