"""
Weather utility — fetches weather data from wttr.in (free, no API key needed).
"""
import requests
from typing import Optional


def get_weather_data(location: str) -> Optional[dict]:
    """Fetch weather data for a location using wttr.in."""
    try:
        resp = requests.get(
            f"https://wttr.in/{location}?format=j1",
            timeout=10,
            headers={"User-Agent": "FarmerAdvisoryAgent/1.0"},
        )
        if resp.status_code != 200:
            return None

        data = resp.json()
        current = data.get("current_condition", [{}])[0]
        forecast = data.get("weather", [])

        # Rain chance from forecast
        rain_chance = 0
        if forecast:
            hourly = forecast[0].get("hourly", [])
            if hourly:
                rain_chance = max(int(h.get("chanceofrain", 0)) for h in hourly)

        return {
            "temperature": float(current.get("temp_C", 25)),
            "humidity": float(current.get("humidity", 50)),
            "condition": current.get("weatherDesc", [{}])[0].get("value", "Clear"),
            "wind_speed": float(current.get("windspeedKmph", 0)),
            "rain_chance": rain_chance,
            "feels_like": float(current.get("FeelsLikeC", 25)),
            "uv_index": float(current.get("uvIndex", 5)),
            "visibility": float(current.get("visibility", 10)),
        }
    except Exception:
        return None
