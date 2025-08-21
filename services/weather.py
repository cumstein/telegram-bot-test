import requests
from config import OPENWEATHER_API_KEY, GEOCODE_URL

def fetch_coordinates(city: str):
    """ گرفتن مختصات شهر از Nominatim """
    try:
        params = {"q": city, "format": "json", "limit": 1}
        r = requests.get(GEOCODE_URL, params=params, headers={"User-Agent": "weather-bot"}, timeout=10)
        data = r.json()
        if not data:
            return None, None
        return data[0]["lat"], data[0]["lon"]
    except:
        return None, None
    
def fetch_daily_forecast(city: str) -> str:
    """ گرفتن وضعیت آب‌وهوا فقط برای امروز (با API رایگان) """
    lat, lon = fetch_coordinates(city)
    if not lat or not lon:
        return f"شهر {city} پیدا نشد ❌"

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=fa"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return "مشکل در گرفتن پیش‌بینی"
    if data.get("cod") != 200:
        return f"خطا در دریافت اطلاعات آب‌وهوا برای {city} ❌"

    temp = data["main"]["temp"]
    temp_min = data["main"].get("temp_min", "-")
    temp_max = data["main"].get("temp_max", "-")
    desc = data["weather"][0]["description"]
    return f"{city}:\n  وضعیت: {desc}\n  دما: {temp}°C\n  بیشینه: {temp_max}°C، کمینه: {temp_min}°C"

def fetch_weather(city: str) -> str:
    """ گرفتن وضعیت آب‌وهوا از OpenWeather """
    lat, lon = fetch_coordinates(city)
    if not lat or not lon:
        return f"شهر {city} پیدا نشد ❌"

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=fa"
    r = requests.get(url, timeout=10)
    data = r.json()
    if data.get("cod") != 200:
        return f"خطا در دریافت اطلاعات آب‌وهوا برای {city} ❌"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return f"آب و هوای {city}:\n🌡 دما: {temp}°C\n🌥 وضعیت: {desc}"
