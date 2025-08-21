import re
from config import BOT_USERNAME

def normalize_text(text: str) -> str:
    """ یکسان‌سازی حروف اب/آب """
    return text.lower().replace("اب", "آب")

def extract_city_from_text(text: str) -> str | None:
    """ گرفتن اسم شهر از جمله «آب و هوای فلان جا» یا «اب و هوای فلان جا» """
    text = normalize_text(text)
    match = re.search(r"آب و هوا(?:ی)?\s+([\u0600-\u06FFa-zA-Z\s]+)", text)
    if match:
        return match.group(1).strip()
    return None

def should_respond_in_group(update) -> bool:
    """ در گروه فقط اگر منشن یا ریپلای باشه جواب بده (به جز کیورد خاص) """
    text = update.message.text
    mentioned = BOT_USERNAME and BOT_USERNAME.lower() in text.lower()
    is_reply_to_bot = (
        update.message.reply_to_message
        and update.message.reply_to_message.from_user.username == BOT_USERNAME.lstrip("@")
    )

    if mentioned or is_reply_to_bot:
        return True
    if "چپ" in normalize_text(text):
        return True
    if extract_city_from_text(text):
        return True
    return False
