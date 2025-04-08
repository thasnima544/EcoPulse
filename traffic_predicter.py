import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
from datetime import datetime

# Read your actual data file
df = pd.read_csv("traffic_data_log.csv")

# Convert categorical 'Day' to numerical
day_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
           'Friday': 4, 'Saturday': 5, 'Sunday': 6}
df['Day'] = df['Day'].map(day_map)

# Features and target
X = df[['Day', 'Hour', 'Duration_Seconds']]
y = df['Duration_Traffic_Seconds']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Predict on new data
now = datetime.now()
current_day = now.strftime("%A")
day_encoded = day_map[current_day]
hour = now.hour
duration_without_traffic = df['Duration_Seconds'].mean()  # Or any static value you prefer

input_data = pd.DataFrame([[day_encoded, hour, duration_without_traffic]], columns=['Day', 'Hour', 'Duration_Seconds'])
predicted_duration = model.predict(input_data)[0]

# Convert to minutes
predicted_minutes = round(predicted_duration / 60, 2)
print(f"Predicted traffic duration: {predicted_minutes} minutes")
