import requests
import csv
import argparse
import logging
import time
import pandas as pd
from prophet import Prophet

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def fetch_data(endpoint, metric, duration):
    """Fetch the data from the API using the given query parameters."""
    url = f"{endpoint}/api/v1/query"
    query = f"{metric}[{duration}]"
    params = {
        'query': query,
    }
    
    logger.info(f"Sending request to {url} with parameters: {params}")
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to fetch data: {response.status_code}")
        return None


def process_data(data):
    """Extract and process the time series data from the API response."""
    if data is None or 'data' not in data or 'result' not in data['data']:
        logger.warning("No time series data found.")
        return []
    
    results = data['data']['result']
    processed_data = []

    for result in results:
        values = result.get('values', [])
        
        for value in values:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(float(value[0])))  # Format timestamp
            cpu_count = value[1]  # CPU count value
            
            # Create a row with only timestamp and cpu_count
            row = {
                'timestamp': timestamp,
                'cpu_count': cpu_count,
            }
            
            processed_data.append(row)
    
    return processed_data


def save_to_csv(data, filename="timeseries_data.csv"):
    """Save the processed data to a CSV file."""
    if not data:
        logger.warning("No data to write to CSV.")
        return
    
    logger.info(f"Saving data to {filename}...")
    
    # Define the fieldnames (only timestamp and cpu_count)
    fieldnames = ['timestamp', 'cpu_count']
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    logger.info(f"Data successfully saved to {filename}.")


def predict_time_series(input_csv="timeseries_data.csv", output_csv="forecasted_data.csv"):
    """Use Facebook Prophet to forecast time series data and save predictions to a CSV file."""
    # Load the CSV data
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        logger.error(f"File {input_csv} not found.")
        return

    # Ensure the data has the correct columns
    if 'timestamp' not in df.columns or 'cpu_count' not in df.columns:
        logger.error("Input CSV must contain 'timestamp' and 'cpu_count' columns.")
        return

    # Rename columns for Prophet
    df.rename(columns={'timestamp': 'ds', 'cpu_count': 'y'}, inplace=True)

    # Convert ds column to datetime
    df['ds'] = pd.to_datetime(df['ds'])

    # Initialize and fit the Prophet model
    model = Prophet()
    model.fit(df)

    # Create a DataFrame for future dates
    future = model.make_future_dataframe(periods=10, freq='H')  # Forecasting 10 future hours

    # Make predictions
    forecast = model.predict(future)

    # Save the forecast to a CSV file
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(output_csv, index=False)
    logger.info(f"Forecasted data successfully saved to {output_csv}.")


def main():
    """Main function to parse arguments and process the data."""
    parser = argparse.ArgumentParser(description="Query and process time series data.")
    parser.add_argument('--endpoint', required=True, help='The API endpoint URL')
    parser.add_argument('--metric', required=True, help='Prometheus metric query')
    parser.add_argument('--duration', required=True, help='Duration for the timeseries query')
    
    args = parser.parse_args()
    
    # Fetch data from the API
    data = fetch_data(args.endpoint, args.metric, args.duration)
    
    # Process and save the data
    processed_data = process_data(data)
    save_to_csv(processed_data)

    # Run time series prediction
    predict_time_series()


if __name__ == "__main__":
    main()


#usage

#python tsdbquery.py --endpoint "http://oass-lb-1331201622.us-east-1.elb.amazonaws.com:9004" --metric 'system_cpu_usage{container="otc-container",service="otel-daemonset-collector"}' --duration "1h"