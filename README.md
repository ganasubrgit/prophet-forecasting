# Dockerized Flask Application for Prometheus Metrics Forecasting

This project provides a Dockerized Flask API that reads Prometheus metrics, uses Facebook Prophet for time series forecasting, and allows downloading the forecast results as a CSV file.

## Features
- Fetches time series data from Prometheus
- Runs Prophet for time series forecasting
- Exposes an API to trigger the forecast process
- Provides an endpoint to download the forecast CSV file

## Prerequisites
- Docker installed
- Prometheus endpoint with accessible metrics

---

## Getting Started

### **1. Build the Docker Image**

```bash
docker build -t prometheus-forecast-api .
```

### **2. Run the Docker Container**

```bash
docker run -d -p 5000:5000 prometheus-forecast-api
```

---

## Usage

### **Trigger Forecast Process**

Send a POST request to `/run-script` with the necessary parameters:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"endpoint": "http://oass-lb-1831201682.us-east-1.elb.amazonaws.com:9004", "metric": "system_cpu_usage{container=\"otc-container\",service=\"otel-daemonset-collector\"}", "duration": "1h"}' \
http://localhost:5000/run-script
```

#### **Parameters:**
- `endpoint`: URL of the Prometheus server
- `metric`: Prometheus metric query
- `duration`: Duration for the time series query (e.g., `1h`, `1d`)

### **Download Forecast CSV**

After the forecast is generated, download the CSV file:

```bash
curl -X GET http://localhost:5000/download-csv --output forecast_data.csv
```

Alternatively, open the following URL in your browser:

```
http://localhost:5000/download-csv
```

---

## Example Workflow

1. Build the Docker image:
   ```bash
   docker build -t prometheus-forecast-api .
   ```
2. Run the container:
   ```bash
   docker run -d -p 5000:5000 prometheus-forecast-api
   ```
3. Trigger the forecast process:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"endpoint": "http://prometheus", "metric": "system_cpu_usage{container=\"otc-container\",service=\"otel-daemonset-collector\"}", "duration": "1h"}' \
   http://localhost:5000/run-script
   ```
4. Download the forecast CSV:
   ```bash
   curl -X GET http://localhost:5000/download-csv --output forecast_data.csv
   ```

---

## Troubleshooting

### **Container Not Running**
Check the container logs:
```bash
docker logs <container_id>
```

### **401 Unauthorized from Prometheus**
Ensure proper authentication is configured when accessing the Prometheus endpoint.

### **Forecast File Not Found**
Make sure the `/run-script` endpoint is called before attempting to download the CSV.

---

## Conclusion
This setup provides an efficient way to fetch and forecast Prometheus metrics using Prophet, with a convenient API interface for automation and data retrieval.

