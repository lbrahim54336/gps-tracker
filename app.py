from flask import Flask, request, send_from_directory
import csv
import os
from datetime import datetime

app = Flask(__name__, static_folder='.')

CSV_FILE = 'gps_data.csv'

# Create CSV file if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'latitude', 'longitude'])


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/location', methods=['POST'])
def location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"📍 Received: {latitude}, {longitude}")

    if latitude and longitude:
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, latitude, longitude])

    return {'status': 'success'}


if __name__ == '__main__':
    # Railway automatically sets a PORT variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
