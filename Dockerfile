# Use the official lightweight Python image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and clean up after
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends tini && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements and install dependencies
COPY requirements.txt .

# Upgrade pip and install necessary Python packages
RUN pip install --no-cache-dir --upgrade pip setuptools cython && \
    pip install --no-cache-dir -r requirements.txt

# Copy the Python script and other necessary files
COPY . .

# Expose the port for the API
EXPOSE 5000

# Set the entrypoint to start the Flask server
ENTRYPOINT ["python", "app.py"]
