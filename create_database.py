import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect('house_automation.db')
cursor = conn.cursor()

# Create EnergyData table
cursor.execute('''
CREATE TABLE IF NOT EXISTS EnergyData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Device_Name TEXT,
    Energy_Consumption REAL,
    Appliance_Time REAL,
    Temp_Settings REAL,
    Solar_Energy REAL,
    Carbon_Emissions REAL
)
''')

# Sample data insertion
devices = [
    ("Refrigerator", 30, 10, 5, 2, 20),
    ("Air Conditioner", 50, 8, 24, 0, 40),
    ("Washing Machine", 25, 2, 30, 1, 15),
    ("Heater", 60, 6, 28, 0, 50),
    ("Lights", 10, 12, 0, 5, 8)
]

cursor.executemany('''
INSERT INTO EnergyData (Device_Name, Energy_Consumption, Appliance_Time, Temp_Settings, Solar_Energy, Carbon_Emissions)
VALUES (?, ?, ?, ?, ?, ?)
''', devices)

conn.commit()
print("Database and table created, sample data inserted.")
conn.close()