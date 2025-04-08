import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
import os

DB_PATH = 'house_automation.db'
PLOT_PATH = 'emissions_plot.png'

def fetch_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM EnergyData", conn)
    conn.close()

    if 'Carbon_Emissions' not in df.columns:
        raise ValueError("Table must contain a 'Carbon_Emissions' column")

    df['Date'] = pd.date_range(start='2025-04-01', periods=len(df))
    df = df.sort_values(by='Date')
    return df

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
    print(f"✅ Plot saved as {PLOT_PATH}")

if __name__ == "__main__":
    df = fetch_data()
    predict_and_plot(df)
