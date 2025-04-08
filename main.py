import random
import os
import matplotlib.pyplot as plt
import qrcode
import base64
from io import BytesIO
import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import timedelta, datetime
from flask import Flask, jsonify, request, send_file

# Initialize the Flask application
app = Flask(__name__)

# Setup file paths
PLOT_PATH = 'emissions_plot.png'
QR_PATH = 'reward_qr.png'

# Fetch Data from SQLite
def fetch_data():
    conn = sqlite3.connect('house_automation.db')
    df = pd.read_sql_query("SELECT * FROM EnergyData", conn)
    conn.close()

    if 'Carbon_Emissions' not in df.columns:
        raise ValueError("Table must contain a 'Carbon_Emissions' column")

    df['Date'] = pd.date_range(start='2025-04-01', periods=len(df))
    df = df.sort_values(by='Date')
    return df

# Prediction function for Carbon Emissions
def predict_and_plot(df):
    df['Date_Ordinal'] = df['Date'].map(datetime.toordinal)
    X = df[['Date_Ordinal']]
    y = df['Carbon_Emissions']

    model = LinearRegression()
    model.fit(X, y)

    last_date = df['Date'].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, 8)]
    future_df = pd.DataFrame([d.toordinal() for d in future_dates], columns=['Date_Ordinal'])
    predicted = model.predict(future_df)

    # Plot actual and predicted values
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], y, label='Actual Emissions', marker='o')
    plt.plot(future_dates, predicted, label='Predicted Emissions', linestyle='--', marker='x')
    plt.xlabel('Date')
    plt.ylabel('Carbon Emissions (kg CO₂)')
    plt.title('Actual vs Predicted Carbon Emissions')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(PLOT_PATH)
    plt.close()

# Generate QR Code (for rewards)
def generate_qr_code():
    qr_text = "You've earned 100 eco points! 🎉 Redeem this voucher now!"
    qr = qrcode.make(qr_text)
    qr.save(QR_PATH)

# Route for Carbon Emission Tracker
@app.route('/tracker', methods=['GET'])
def tracker():
    # Fetch and process data
    df = fetch_data()
    predict_and_plot(df)

    # Generate QR code
    generate_qr_code()

    # Convert image to base64
    with open(PLOT_PATH, "rb") as img_file:
        plot_image = base64.b64encode(img_file.read()).decode('utf-8')

    with open(QR_PATH, "rb") as qr_file:
        qr_image = base64.b64encode(qr_file.read()).decode('utf-8')

    # Return JSON response with plot and QR code
    return jsonify({
        'plot': plot_image,
        'qr_code': qr_image,
        'message': "Data processed successfully!"
    })

# Route for Traffic Prediction with Random Data
@app.route('/predict-traffic', methods=['GET'])
def predict_traffic():
    # Get the current hour to simulate traffic changes based on time of day
    current_hour = datetime.now().hour

    # Simulate a changing traffic pattern depending on the time of day
    if current_hour < 6:  # Early morning (less traffic)
        predicted_duration = random.randint(15, 30)  # 15 to 30 minutes
    elif current_hour < 9:  # Morning rush hour
        predicted_duration = random.randint(40, 60)  # 40 to 60 minutes
    elif current_hour < 12:  # Mid-morning
        predicted_duration = random.randint(25, 45)  # 25 to 45 minutes
    elif current_hour < 15:  # Early afternoon
        predicted_duration = random.randint(20, 35)  # 20 to 35 minutes
    elif current_hour < 18:  # Evening rush hour
        predicted_duration = random.randint(50, 70)  # 50 to 70 minutes
    elif current_hour < 21:  # Night time (less traffic)
        predicted_duration = random.randint(20, 40)  # 20 to 40 minutes
    else:  # Late night
        predicted_duration = random.randint(10, 25)  # 10 to 25 minutes

    # Return JSON with the predicted traffic duration and current time details
    return jsonify({
        'predicted_duration': predicted_duration,
        'unit': 'minutes',
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'message': "Traffic prediction completed successfully!"
    })

# To serve static files like images if needed
@app.route('/static/<filename>', methods=['GET'])
def serve_static_files(filename):
    return send_file(os.path.join('static', filename))

if __name__ == '__main__':
    # Make sure the static folder exists
    os.makedirs("static", exist_ok=True)

    # Run the Flask app
    app.run(debug=True)
