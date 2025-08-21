import os
from typing import Final
from dotenv import load_dotenv

load_dotenv()

TOKEN: Final = os.getenv("TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")
OPENWEATHER_API_KEY: Final = os.getenv("OPENWEATHER_API_KEY")
GEOCODE_URL: Final = "https://nominatim.openstreetmap.org/search"

# حافظه موقت (کاربرانی که بات ازشون اسم شهر خواسته)
pending_city_request = {}
