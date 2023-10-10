#!/usr/bin/env python3

import json
import requests
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ICON_MAP = {
    "01d": "☀️",
    "02d": "⛅️",
    "03d": "☁️",
    "04d": "☁️",
    "09d": "🌧️",
    "10d": "🌦️",
    "11d": "⛈️",
    "13d": "🌨️",
    "50d": "🌫",
}


def main():
    apikey = os.getenv("WAYBAR_WEATHER_APIKEY")
    lat = os.getenv("WAYBAR_WEATHER_LAT", "52.52")
    lon = os.getenv("WAYBAR_WEATHER_LON", "13.38")
    units = os.getenv("WAYBAR_WEATHER_UNITS", "metric")
    exclude = os.getenv("WAYBAR_WEATHER_EXCLUDE", "minutely,daily")

    data = {}
    try:
        url = (f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}"
               f"&lon={lon}&units={units}&exclude={exclude}&appid={apikey}")
        weather = requests.get(url).json()

    except Exception as e:
        return print({})

    if weather.get("cod"):
        data["text"] = "[weather] Error {}: {}".format(
            weather.get("cod"), weather.get("message")
        )
        data["class"] = "weather"
        print(json.dumps(data))
        # sys.exit(data["text"])
        sys.exit()

    temp = weather["current"]["temp"]
    icon = ICON_MAP.get(weather["current"]["weather"][0]["icon"], "")
    feels_like = weather["current"]["feels_like"]
    humidity = weather["current"]["humidity"]
    pressure = weather["current"]["pressure"]
    sunrise = datetime.fromtimestamp(
        weather["current"]["sunrise"], ZoneInfo(weather["timezone"])
    ).strftime("%H:%M")
    sunset = datetime.fromtimestamp(
        weather["current"]["sunset"], ZoneInfo(weather["timezone"])
    ).strftime("%H:%M")
    wind_speed = weather["current"]["wind_speed"]

    data["text"] = f"{icon} {temp}°C"
    data["tooltip"] = f"""Feels like {feels_like}°C
Pressure {pressure}
Humidity {humidity}
Sunrise {sunrise}
Sunset {sunset}
Wind speed {wind_speed}Km/h"""
    data["class"] = "weather"

    print(json.dumps(data))


if __name__ == "__main__":
    main()
