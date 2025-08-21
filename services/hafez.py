from hafez import omen

def get_random_hafez():
    try:
        poem = omen()
        # poem is a dict with keys: 'poem', 'ghazal', 'interpretation', etc.
        title = poem.get("title", "")
        ghazal = poem.get("ghazal", "")
        interpretation = poem.get("interpretation", "")
        # You can format as you like:
        return f"{title}\n{ghazal}\n\nتفسیر: {interpretation}"
    except Exception as e:
        print("Hafez error:", e)
        return ""