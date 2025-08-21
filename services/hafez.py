from hafez import omen
import random

def get_random_hafez():
    try:
        poem = omen()
        print("OMEN DATA:", poem)  # برای دیباگ
        lines = poem.get("poem", [])
        if not lines or len(lines) < 2:
            print("Poem is empty or too short!")
            return ""
        idx = random.randint(0, len(lines) - 2)
        couplet = f"{lines[idx]}\n{lines[idx+1]}"
        omens = []
        for name in ["کامی", "میلاد", "مهدی"]:
            omen_data = omen()
            print(f"{name} OMEN:", omen_data)  # برای دیباگ
            interpretation = omen_data.get("interpretation", "")
            omens.append(f"فال {name}:\n{interpretation}")
        omens_text = "\n\n".join(omens)
        return f"{couplet}\n\n{omens_text}"
    except Exception as e:
        print("Hafez error:", e)
        return ""