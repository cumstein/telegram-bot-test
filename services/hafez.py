import requests

HAFEZ_API = "https://hafez-dxle.onrender.com/fal"

def get_random_hafez():
    try:
        r = requests.get(HAFEZ_API, timeout=5)
        data = r.json()
        print("Hafez API response:", data)  # لاگ برای دیباگ
        return data.get("text", "")
    except Exception as e:
        print("Hafez API error:", e)
        return ""