import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set Seaborn theme
sns.set_theme(style="whitegrid")

# Load smart home energy data
home_energy = pd.read_csv("smart_home_energy_consumption_large.csv")

# Load EV charging station data
charging_stations = pd.read_csv("Electric and Alternative Fuel Charging Stations.csv", low_memory=False)

# Process smart home energy data
home_summary = home_energy[['Date', 'Outdoor Temperature (°C)', 'Energy Consumption (kWh)']].copy()
home_summary['Date'] = pd.to_datetime(home_summary['Date'], errors='coerce')
home_summary.dropna(subset=['Date'], inplace=True)
home_summary['Month'] = home_summary['Date'].dt.to_period('M')
monthly_energy = home_summary.groupby('Month')['Energy Consumption (kWh)'].sum().reset_index()

# Process EV station data
ev_summary = charging_stations.groupby('State').size().reset_index(name='Station Count')
top_states = ev_summary.sort_values(by='Station Count', ascending=False).head(10)

# Create directory for images
os.makedirs("static", exist_ok=True)

# Plot: Monthly energy consumption
plt.figure(figsize=(12, 6))
sns.barplot(data=monthly_energy, x='Month', y='Energy Consumption (kWh)', palette="Reds_r")
plt.title("Monthly Smart Home Energy Consumption")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("static/monthly_energy.png")
plt.close()

# Plot: Top 10 states by EV stations
plt.figure(figsize=(10, 6))
sns.barplot(data=top_states, x='State', y='Station Count', palette="Greens")
plt.title("Top 10 States by EV Charging Stations")
plt.tight_layout()
plt.savefig("static/ev_stations.png")
plt.close()

# Generate simple badge info (for HTML)
badge_info = ""
for i, row in top_states.iterrows():
    state = row['State']
    if i < 3:
        badge = 'gold'
    elif i < 7:
        badge = 'silver'
    else:
        badge = 'bronze'
    badge_info += f'<li class="badge {badge}">{state}: {row["Station Count"]} stations</li><br>\n'

# Load and populate HTML template
with open("template.html", "r", encoding="utf-8") as template_file:
    html_template = template_file.read()

html_output = html_template.replace("{{BADGES}}", badge_info)

with open("city_energy_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("✅ Dashboard generated successfully: city_energy_dashboard.html")
