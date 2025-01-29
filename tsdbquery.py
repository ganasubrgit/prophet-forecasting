import argparse
import requests
import pandas as pd
import logging

def fetch_prometheus_data(endpoint, metric, timeseries, duration):
    """
    Fetches time series data from a Prometheus endpoint.

    Args:
        endpoint: The URL of the Prometheus endpoint.
        metric: The name of the metric to query.
        timeseries: The start time of the query in Prometheus expression format (e.g., 'now() - 1h').
        duration: The duration of the query in Prometheus expression format (e.g., '1h').

    Returns:
        A pandas DataFrame containing the fetched data.
    """

    try:
        query = f"{metric}[{timeseries}:{duration}]"
        url = f"{endpoint}/api/v1/query_range"
        params = {
            'query': query,
            'start': timeseries,
            'end': f"{timeseries} + {duration}",
            'step': '1s'  # Adjust step size as needed
        }

        logging.info(f"Fetching data for metric '{metric}' from {endpoint}")
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()['data']['result'][0]['values']
        logging.info(f"Successfully fetched {len(data)} data points")

        df = pd.DataFrame(data, columns=['ds', 'y'])
        df['ds'] = pd.to_datetime(df['ds'], unit='s') 
        return df

    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Prometheus data and save to CSV.")
    parser.add_argument("--endpoint", type=str, required=True, help="Prometheus endpoint URL")
    parser.add_argument("--metric", type=str, required=True, help="Metric name")
    parser.add_argument("--timeseries", type=str, required=True, help="Start time in Prometheus expression format")
    parser.add_argument("--duration", type=str, required=True, help="Duration in Prometheus expression format")
    parser.add_argument("--output", type=str, default="prometheus_data.csv", help="Output CSV file name")
    parser.add_argument("--log_level", type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Logging level")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=args.log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        df = fetch_prometheus_data(args.endpoint, args.metric, args.timeseries, args.duration)
        df.to_csv(args.output, index=False)
        logging.info(f"Data saved to {args.output}")

    except Exception as e:
        logging.error(f"Error processing data: {e}")
        
        

# python fetch_prometheus_data.py --endpoint "http://your_prometheus_endpoint:9090" \
#                                --metric "your_metric_name" \
#                                --timeseries "now() - 1h" \
#                                --duration "1h"