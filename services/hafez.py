from hafez import omen
import random

def get_random_hafez():
    try:
        poem = omen()
        ghazal = poem.get("ghazal", "")
        if not ghazal:
            return ""
        lines = [line.strip() for line in ghazal.split("\n") if line.strip()]
        # انتخاب دو خط پشت سر هم (یک بیت)
        if len(lines) < 2:
            couplet = "\n".join(lines)
        else:
            idx = random.randint(0, len(lines) - 2)
            couplet = f"{lines[idx]}\n{lines[idx+1]}"
        # سه فال جداگانه
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