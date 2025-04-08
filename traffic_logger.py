import requests
import csv
import datetime

# Constants
API_KEY = 'AIzaSyAloHVsXLCCTAM-P7RFGsP_lXyMgKyp1Jk'
ORIGIN = '10.8626,76.8813'
DESTINATION = '10.9758,76.9590'
CSV_FILE = 'traffic_data_log.csv'

# Function to get traffic data
def get_traffic_data():
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'origin': ORIGIN,
        'destination': DESTINATION,
        'departure_time': 'now',
        'traffic_model': 'best_guess',
        'key': API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        route = data['routes'][0]['legs'][0]
        duration = route['duration']['value']  # in seconds
        duration_in_traffic = route['duration_in_traffic']['value']  # in seconds
        return duration, duration_in_traffic
    else:
        print('Error:', data['status'])
        return None, None

# Function to log data
def log_traffic_data():
    duration, duration_in_traffic = get_traffic_data()
    if duration is None:
        print("Failed to retrieve traffic data.")
        return

    now = datetime.datetime.now()
    row = [now.strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%A'), now.hour, duration, duration_in_traffic]

    file_exists = False
    try:
        with open(CSV_FILE, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Day', 'Hour', 'Duration_Seconds', 'Duration_Traffic_Seconds'])
        writer.writerow(row)

    print("Traffic data logged successfully.")

# Run the logger once
log_traffic_data()
