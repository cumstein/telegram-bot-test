import os
import re
import requests
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# ---------------------- ENV ----------------------
load_dotenv()
TOKEN: Final = os.getenv("TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")
OPENWEATHER_API_KEY: Final = os.getenv("OPENWEATHER_API_KEY")
GEOCODE_URL: Final = "https://nominatim.openstreetmap.org/search"

# حافظه موقت (کاربرانی که بات ازشون اسم شهر خواسته)
pending_city_request = {}

# ---------------------- WEATHER ----------------------
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

# ---------------------- HELPERS ----------------------
def normalize_text(text: str) -> str:
    """ یکسان‌سازی حروف اب/آب """
    return text.lower().replace("اب", "آب")

def extract_city_from_text(text: str) -> str | None:
    """ از متن کاربر دنبال «آب و هوای فلان‌جا» بگرد """
    match = re.search(r"آب و هوای\s+([\u0600-\u06FFa-zA-Z\s]+)", text)
    if match:
        return match.group(1).strip()
    return None

def should_respond_in_group(update: Update) -> bool:
    """ در گروه فقط اگر منشن یا ریپلای باشه جواب بده (به جز کیورد خاص) """
    text = update.message.text
    mentioned = BOT_USERNAME and BOT_USERNAME.lower() in text.lower()
    is_reply_to_bot = (
        update.message.reply_to_message
        and update.message.reply_to_message.from_user.username == BOT_USERNAME.lstrip("@")
    )

    # اگر منشن یا ریپلای → جواب بده
    if mentioned or is_reply_to_bot:
        return True

    # استثنا: اگر «چپ» یا «آب و هوای فلان‌جا» تو متن باشه → جواب بده
    if "چپ" in text or extract_city_from_text(text):
        return True

    # در غیر این صورت → هیچی نگو
    return False

# ---------------------- RESPONSES ----------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_type = update.message.chat.type
    text = normalize_text(update.message.text)

    # گروه → اول بررسی کنیم لازمه جواب بده یا نه
    if chat_type in ["group", "supergroup"]:
        if not should_respond_in_group(update):
            return

    # اگر تو pending باشه → این متن اسم شهر حساب میشه
    if pending_city_request.get(user_id):
        pending_city_request.pop(user_id)
        reply = fetch_weather(text)
        await update.message.reply_text(reply)
        return

    # حالت «آب و هوای فلان‌جا»
    city = extract_city_from_text(text)
    if city:
        reply = fetch_weather(city)
        await update.message.reply_text(reply)
        return

    # حالت «آب و هوا»
    if "آب و هوا" in text:
        pending_city_request[user_id] = True
        await update.message.reply_text("بگو اسم شهری که میخوای 🌍")
        return

    # سلام و غیره
    if "درود" in text:
        await update.message.reply_text("درود عمویی")
    elif "چطوری" in text:
        await update.message.reply_text("مخلصم")
    elif "سلام" in text:
        await update.message.reply_text("سلام رو نمیفهمم باید بگی درود")
    elif "چپ" in text:
        await update.message.reply_text("چپ هرگز نفهمید!")
    else:
        return

# ---------------------- COMMANDS ----------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("درود! من بات غیرهوشمندم 🤖")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("بگو: آب و هوای تهران 🌍 یا فقط بگو آب و هوا تا راهنمایی‌ت کنم.")

async def chap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("چپ هرگز نفهمید")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.args:
        city = " ".join(context.args)
        reply = fetch_weather(city)
        await update.message.reply_text(reply)
    else:
        pending_city_request[user_id] = True
        await update.message.reply_text("کدوم شهر؟ 🌍")

# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    print("bot is starting...")

    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("chap", chap_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("polling...")
    app.run_polling(poll_interval=3)
