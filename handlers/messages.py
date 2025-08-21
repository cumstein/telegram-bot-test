from telegram import Update
from telegram.ext import ContextTypes
from config import pending_city_request
from services.weather import fetch_weather
from utils.helpers import normalize_text, extract_city_from_text, should_respond_in_group

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_type = update.message.chat.type
    text = normalize_text(update.message.text)

    if chat_type in ["group", "supergroup"]:
        if not should_respond_in_group(update):
            return

    if pending_city_request.get(user_id):
        pending_city_request.pop(user_id)
        reply = fetch_weather(text)
        await update.message.reply_text(reply)
        return

    city = extract_city_from_text(text)
    if city:
        reply = fetch_weather(city)
        await update.message.reply_text(reply)
        return

    if "آب و هوا" in text:
        pending_city_request[user_id] = True
        await update.message.reply_text("بگو اسم شهری که میخوای 🌍")
        return

    if "درود" in text:
        await update.message.reply_text("درود عمویی")
    elif "چطوری" in text:
        await update.message.reply_text("مخلصم")
    elif "سلام" in text:
        await update.message.reply_text("سلام رو نمیفهمم باید بگی درود")
    elif "چپ" in text:
        await update.message.reply_text("چپ هرگز نفهمید!")
    else:
        await update.message.reply_text("متاسفانه نمیفهمم چی میگی. همونطور که چپ هرگز نفهمید!")
