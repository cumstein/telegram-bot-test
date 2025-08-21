import requests

HAFEZ_API = "https://hafez-dxle.onrender.com/fal"

def get_random_hafez():
    try:
        r = requests.get(HAFEZ_API, timeout=5)
        data = r.json()
        # فرض بر اینکه پاسخ یه شی با کلید "text" باشه
        return data.get("text", "")
    except:
        return ""
