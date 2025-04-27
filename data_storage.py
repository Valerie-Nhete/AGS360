import csv
import os
from datetime import datetime

DATA_FILE = "agrisense_data.csv"
daily_data_log = []

def store_daily_data(data):
    daily_data_log.append(data)

def export_data_to_csv():
    if not daily_data_log:
        print("No data to export.")
        return

    file_exists = os.path.isfile(DATA_FILE)

    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Weather", "Temperature", "Soil Moisture",
                             "Microbial Health", "Peer Data", "Crop Suggestions",
                             "Yield Estimate", "Profit Estimate"])
        for data in daily_data_log:
            writer.writerow([
                data["date"],
                data["weather"],
                data["temperature"],
                data["soil_moisture"],
                data["microbial_health"],
                data["peer_data"],
                ", ".join(data["crop_suggestions"]),
                data["yield_estimate"],
                data["profit_estimate"]
            ])