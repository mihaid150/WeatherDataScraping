import csv
import os
from DataScraper import fetch_data_from_website, fetch_no_of_days

# Define a dictionary to map month numbers to their names
month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
               7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}


def mbar_to_mm_hg(pressure_in_mbar):
    conversion_factor = 0.750062
    pressure_in_mm_hg = pressure_in_mbar * conversion_factor
    return pressure_in_mm_hg


def extract_numeric_value(text):
    # Extract numeric value from a string with possible units
    try:
        if "°C" in text:
            numeric_value = float(text.replace(" °C", "").strip())
            return "{:.2f}".format(numeric_value)  # Format to two decimal places
        elif "%" in text:
            numeric_value = float(text.replace("%", "").strip())
            return "{:.2f}".format(numeric_value)  # Format to two decimal places
        elif "km/h" in text:
            numeric_value = float(text.replace(" km/h", "").strip())
            return "{:.2f}".format(numeric_value)  # Format to two decimal places
        elif "mbar" in text:
            numeric_value = float(text.replace(" mbar", "").strip())
            return numeric_value
        elif "No wind" in text:
            return "{:.2f}".format(0)  # Format to two decimal places
    except ValueError:
        return None


def generate_csv(month, year):
    no_of_days = fetch_no_of_days(month, year)

    # Create a folder for the current year if it doesn't exist within the year folder
    year_folder = os.path.join("output", str(year))
    os.makedirs(year_folder, exist_ok=True)

    for i in range(no_of_days):
        table_data = fetch_data_from_website(i + 1, month, year)
        if i + 1 < 10:
            day = "0" + str(i + 1)
        else:
            day = str(i + 1)
        test_data_date = str(month) + "_" + day + "_" + str(year)

        # Create a folder for the current month if it doesn't exist within the year folder
        month_folder = os.path.join(year_folder, month_names[month])
        os.makedirs(month_folder, exist_ok=True)

        # Create a CSV writer object within the month folder
        file_name = os.path.join(month_folder, test_data_date + ".csv")
        with open(file_name, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header row.
            header = ["Date Time", "Weather status", "Temperature (°C)", "Wind Speed (km/h)", "Humidity (%)",
                      "Pressure (mmHg)"]
            writer.writerow(header)

            for row in table_data:
                time_value = row[0]
                date_time = test_data_date.replace("_", "/") + " " + time_value

                temperature = extract_numeric_value(row[1])
                if temperature is None:
                    continue
                weather_status = row[2].replace(".", "")
                if weather_status is None:
                    continue
                wind_speed = extract_numeric_value(row[3])
                if wind_speed is None:
                    continue
                humidity = extract_numeric_value(row[5])
                if humidity is None:
                    continue
                row_pressure = extract_numeric_value(row[6])
                if row_pressure is None:
                    continue
                pressure = "{:.2f}".format(mbar_to_mm_hg(row_pressure))
                if pressure is None:
                    continue
                values = [date_time, weather_status, temperature, wind_speed, humidity, pressure]
                writer.writerow(values)
            print("Successfully written into csv file for day " + day + "!")
