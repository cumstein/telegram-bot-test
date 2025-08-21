from hafez import omen
import random

def get_random_hafez():
    try:
        poem = omen()
        lines = poem.get("poem", [])
        if not lines or len(lines) < 2:
            print("Poem is empty or too short!")
            return ""
        idx = random.randint(0, len(lines) - 2)
        couplet = f"{lines[idx]}\n{lines[idx+1]}"
        omens = []
        for name in ["کامی", "میلاد", "مهدی"]:
            omen_data = omen()
            interpretation = omen_data.get("interpretation", "")
            omens.append(f"فال {name}:\n{interpretation}")
        omens_text = "\n\n".join(omens)
        return f"{couplet}\n\n{omens_text}"
    except Exception as e:
        print("Hafez error:", e)
        return ""