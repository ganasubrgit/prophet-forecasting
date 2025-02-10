from flask import Flask, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)

OUTPUT_FILE = "forecasted_data.csv"

@app.route('/run-script', methods=['POST'])
def run_script():
    """Run the time series script based on API request."""
    endpoint = request.json.get('endpoint')
    metric = request.json.get('metric')
    duration = request.json.get('duration')

    if not all([endpoint, metric, duration]):
        return jsonify({"error": "Missing required parameters (endpoint, metric, duration)"}), 400

    try:
        # Run the Python script as a subprocess
        result = subprocess.run(
            ["python", "tsdbquery.py", "--endpoint", endpoint, "--metric", metric, "--duration", duration],
            capture_output=True, text=True
        )
        
        return jsonify({"stdout": result.stdout, "stderr": result.stderr})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download-csv', methods=['GET'])
def download_csv():
    """Serve the CSV file for download."""
    if not os.path.exists(OUTPUT_FILE):
        return jsonify({"error": "CSV file not found. Please run the script first."}), 404

    return send_file(OUTPUT_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


# usage
# curl -X POST -H "Content-Type: application/json" \
# -d '{"endpoint": "http://example.com", "metric": "cpu_usage", "duration": "1h"}' \
# http://localhost:5000/run-script
