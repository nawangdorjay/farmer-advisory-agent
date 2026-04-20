"""
Farmer Advisory Agent — Tool Functions
Each tool returns structured data for the LLM to use.
"""
import json
import os
import requests
from pathlib import Path
from utils.weather import get_weather_data
from utils.language import detect_language, SUPPORTED_LANGUAGES

DATA_DIR = Path(__file__).parent.parent / "data"


def _load_json(filename: str) -> dict:
    """Load a JSON data file."""
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_crop_info(crop_name: str) -> dict:
    """Get detailed crop information."""
    crops = _load_json("crops.json")
    crop_key = crop_name.lower().strip()

    if crop_key in crops:
        return {"found": True, "crop": crop_key, **crops[crop_key]}

    # Fuzzy match
    for key in crops:
        if crop_key in key or key in crop_key:
            return {"found": True, "crop": key, **crops[key]}

    return {
        "found": False,
        "message": f"No detailed data for '{crop_name}'. Try: rice, wheat, cotton, sugarcane, maize, bajra, jowar, mustard, groundnut, chickpea, tomato, potato, onion.",
    }


def get_weather_advisory(location: str, crop: str = None) -> dict:
    """Get weather-based farming advisory."""
    weather = get_weather_data(location)
    if not weather:
        return {"error": f"Could not fetch weather for {location}"}

    temp = weather.get("temperature", 25)
    humidity = weather.get("humidity", 50)
    condition = weather.get("condition", "clear")
    rain_chance = weather.get("rain_chance", 0)

    advisories = []

    # Temperature-based advice
    if temp > 40:
        advisories.append("🌡️ Extreme heat alert! Increase irrigation frequency. Avoid midday fieldwork.")
        advisories.append("Use mulching to retain soil moisture.")
    elif temp > 35:
        advisories.append("🌡️ Hot weather. Ensure adequate irrigation, especially for seedlings.")
    elif temp < 5:
        advisories.append("❄️ Frost risk! Protect sensitive crops with covers. Avoid irrigation at night.")
    elif temp < 15:
        advisories.append("🌡️ Cool weather. Growth may slow. Adjust fertilizer application timing.")

    # Humidity-based advice
    if humidity > 85:
        advisories.append("💧 High humidity — watch for fungal diseases. Ensure good air circulation.")
    elif humidity < 30:
        advisories.append("💧 Low humidity — increase irrigation frequency. Consider drip irrigation.")

    # Rain advice
    if rain_chance > 70:
        advisories.append("🌧️ Heavy rain expected. Delay fertilizer/pesticide application. Check drainage.")
        advisories.append("Harvest ready crops if any.")
    elif rain_chance > 40:
        advisories.append("🌧️ Rain likely. Prepare drainage channels. Hold off on spraying.")

    # Crop-specific
    if crop:
        crops = _load_json("crops.json")
        crop_data = crops.get(crop.lower(), {})
        if crop_data:
            water_needs = crop_data.get("water_needs", "moderate")
            if water_needs == "high" and humidity < 40:
                advisories.append(f"🌾 {crop.title()} needs high water. Ensure irrigation is sufficient in dry conditions.")

    return {
        "location": location,
        "weather": weather,
        "advisories": advisories if advisories else ["✅ Conditions are normal. Continue regular farming activities."],
    }


def get_pest_info(crop_name: str, symptom: str = "") -> dict:
    """Get pest/disease info for a crop."""
    pests = _load_json("pests.json")
    crop_key = crop_name.lower().strip()

    if crop_key not in pests:
        # Fuzzy match
        for key in pests:
            if crop_key in key or key in crop_key:
                crop_key = key
                break
        else:
            return {"found": False, "message": f"No pest data for '{crop_name}'."}

    crop_pests = pests[crop_key]

    if symptom:
        symptom_lower = symptom.lower()
        matched = []
        for pest in crop_pests:
            if any(s in symptom_lower for s in pest.get("symptoms_keywords", [])):
                matched.append(pest)
        if matched:
            return {"found": True, "crop": crop_key, "matches": matched}

    return {"found": True, "crop": crop_key, "common_pests": crop_pests}


def get_government_schemes(query: str, state: str = None) -> dict:
    """Get government scheme info."""
    schemes = _load_json("schemes.json")
    query_lower = query.lower()

    matched = []
    for scheme in schemes:
        name_lower = scheme.get("name", "").lower()
        desc_lower = scheme.get("description", "").lower()
        keywords = scheme.get("keywords", [])

        if (query_lower in name_lower or
            query_lower in desc_lower or
            any(query_lower in kw for kw in keywords)):
            if state and scheme.get("states") and state.lower() not in [s.lower() for s in scheme["states"]]:
                continue
            matched.append(scheme)

    if not matched:
        # Return all central schemes as fallback
        matched = [s for s in schemes if s.get("type") == "central"]

    return {"query": query, "state": state, "schemes": matched[:5]}


def get_market_prices(crop_name: str, state: str = None) -> dict:
    """Get market prices (simulated data structure for production API integration)."""
    prices = _load_json("market_prices.json")
    crop_key = crop_name.lower().strip()

    if crop_key in prices:
        data = prices[crop_key]
        if state and state.lower() in data.get("state_prices", {}):
            return {
                "crop": crop_key,
                "state": state,
                "price": data["state_prices"][state.lower()],
                "unit": data.get("unit", "per quintal"),
                "trend": data.get("trend", "stable"),
                "note": "Prices are indicative. Check local mandi for actual rates.",
            }
        return {
            "crop": crop_key,
            "national_avg": data.get("national_avg"),
            "unit": data.get("unit", "per quintal"),
            "trend": data.get("trend", "stable"),
            "price_range": data.get("range"),
            "note": "Prices are indicative. Check eNAM (enam.gov.in) for live prices.",
        }

    return {"found": False, "message": f"No price data for '{crop_name}'. Check eNAM.gov.in for live mandi prices."}


def get_crop_calendar(region: str, crop_name: str = None) -> dict:
    """Get seasonal crop calendar."""
    calendar = _load_json("crop_calendar.json")
    region_lower = region.lower().strip()

    if region_lower in calendar:
        data = calendar[region_lower]
        if crop_name:
            crop_key = crop_name.lower()
            if crop_key in data:
                return {"region": region, "crop": crop_key, "calendar": data[crop_key]}
            return {"region": region, "message": f"No calendar data for '{crop_name}' in {region}."}
        return {"region": region, "calendar": data}

    # Fallback: return North India calendar
    fallback = calendar.get("north india", {})
    return {
        "region": "North India (default)",
        "calendar": fallback,
        "note": f"No specific calendar for '{region}'. Showing North India schedule.",
    }
