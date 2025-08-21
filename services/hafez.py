import requests

HAFEZ_API = "https://hafez-dxle.onrender.com/fal"

def get_random_hafez():
    try:
        r = requests.get(HAFEZ_API, timeout=5)
        data = r.json()
        print("Hafez API response:", data)  # لاگ برای دیباگ
        title = data.get("title", "")
        interpreter = data.get("interpreter", "")
        if title or interpreter:
            return f"{title}\n{interpreter}"
        return ""
    except Exception as e:
        print("Hafez API error:", e)
        return ""