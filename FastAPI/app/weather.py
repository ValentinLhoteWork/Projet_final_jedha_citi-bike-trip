import os
import http.client
import json

import pandas as pd
from dotenv import load_dotenv

# Charger les variables du fichier .env

load_dotenv()

def get_weather(request_datetime):
    api_key = os.getenv(
        "RAPIDAPI_KEY"
        )
    if not api_key:
        raise ValueError(
            "RAPIDAPI_KEY is not defined."
            )
    conn = http.client.HTTPSConnection(
        "meteostat.p.rapidapi.com"
        )
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host":
        "meteostat.p.rapidapi.com"
        }
    
    date_str = request_datetime.strftime(
        "%Y-%m-%d"
        )
    
    url = (
        f"/stations/hourly"
        f"?station=KNYC0"
        f"&start={date_str}"
        f"&end={date_str}"
        f"&tz=America/New_York"
        )

    conn.request(
        "GET",
        url,
        headers=headers
        )
    
    response = conn.getresponse()
    if response.status != 200:
        raise ValueError(
            f"Weather API error: "
            f"{response.status}"
            )
    
    weather_json = json.loads(
        response.read().decode("utf-8")
        )
    
    
    data = weather_json.get(
        "data",
        []
        )
    
    if not data:
        raise ValueError(
            "No weather data available."
            )
    weather_df = pd.DataFrame(data)

# ---------------------------------
# Sélectionner l'heure demandée
# ---------------------------------

    weather_df["time"] = pd.to_datetime(
        weather_df["time"]
        )
    
    target_hour = request_datetime.hour
    weather_df = weather_df[
        weather_df["time"].dt.hour
        == target_hour
        ]
    
    if weather_df.empty:
        raise ValueError(
            "No weather observation "
            "available for requested hour."
            )
    
    weather_df = weather_df.iloc[
        [0]
        ].copy()

# ---------------------------------
# Renommer les variables
# ---------------------------------

    weather_df = weather_df.rename(
        columns={
            "rhum":
            "relative_humidity",
            "prcp":
            "precipitation_total",
            "wspd":
            "average_wind_speed"
            }
        )

# ---------------------------------
# Coco group
# ---------------------------------

    coco_mapping = {
        1: "Clear",
        2: "Fair",
        3: "Cloudy",
        4: "Overcast",
        5: "Fog",
        6: "Freezing Fog",
        7: "Light Rain",
        8: "Rain",
        9: "Heavy Rain",
       10: "Freezing Rain",
       11: "Heavy Freezing Rain",
       12: "Sleet",
       13: "Heavy Sleet",
       14: "Snow",
       15: "Heavy Snow",
       16: "Rain Shower",
       17: "Heavy Rain Shower",
       18: "Snow Shower",
       19: "Heavy Snow Shower",
       20: "Storm",
       21: "Hail",
       22: "Thunderstorm"
       }

    weather_df["coco_group"] = (
        weather_df["coco"]
        .map(coco_mapping)
        )
    keep_columns = [
        "temp",
        "relative_humidity",
        "precipitation_total",
        "average_wind_speed",
        "coco",
        "coco_group"
        ]
    return weather_df[
        keep_columns
        ]

