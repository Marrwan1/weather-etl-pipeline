import requests
import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

CITIES = ["Cairo", "Alexandria", "Dubai", "London", "New York"]

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def fetch_city_weather(city: str) -> dict:
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()
        logger.info(f"Successfully fetched weather for {city}")
        return data

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error for {city}: {e}")
        return None

    except requests.exceptions.ConnectionError:
        logger.error(f"Connection Error for {city}")
        return None


def fetch_all_cities() -> list:
    results = []

    for city in CITIES:
        data = fetch_city_weather(city)
        if data:
            results.append(data)

    logger.info(f"fetched {len(results)}/{len(CITIES)} cities successfully")
    return results


if __name__ == "__main__":
    data = fetch_all_cities()
    print(json.dumps(data[0], indent=2))
