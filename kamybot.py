import os
import re
import requests
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# ---------------------- ENV ----------------------
load_dotenv()

TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")
OPENWEATHER_API_KEY: Final = os.getenv("OPENWEATHER_API_KEY")
GEOCODE_URL: Final = "https://nominatim.openstreetmap.org/search"

# ---------------------- WEATHER ----------------------
async def get_city_coordinates(city: str):
    try:
        params = {"q": city, "format": "json", "limit": 1}
        response = requests.get(GEOCODE_URL, params=params, timeout=10, headers={"User-Agent": "kamybot"})
        data = response.json()
        if not data:
            return None, None
        return data[0]["lat"], data[0]["lon"]
    except Exception as e:
        print(f"Error in get_city_coordinates: {e}")
        return None, None

async def get_weather(city: str) -> str:
    lat, lon = await get_city_coordinates(city)
    if not lat or not lon:
        return f"شهر {city} پیدا نشد ❌"

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=fa"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("cod") != 200:
            return f"خطا در دریافت اطلاعات آب‌وهوا برای {city} ❌"

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"آب و هوای {city}:\n🌡 دما: {temp}°C\n🌥 وضعیت: {desc}"
    except Exception as e:
        print(f"Error in get_weather: {e}")
        return "خطایی در دریافت آب‌وهوا رخ داد ❌"

# ---------------------- RESPONSES ----------------------
async def handle_response(text: str) -> str:
    processed: str = text.lower().replace("اب", "آب")  # فرق "اب" و "آب"

    # حالت: "آب و هوای {شهر}"
    match = re.search(r"آب و هوای\s+([\u0600-\u06FFa-zA-Z\s]+)", processed)
    if match:
        city = match.group(1).strip()
        return await get_weather(city)

    # حالت: فقط آب و هوا
    if "آب و هوا" in processed:
        return "بگو اسم شهری که میخوای 🌍"

    if "درود" in processed:
        return "درود عمویی"
    if "چطوری" in processed:
        return "مخلصم"
    if "سلام" in processed:
        return "سلام رو نمیفهمم باید بگی درود"
    if "چپ" in processed:
        return "چپ هرگز نفهمید!"
    
    return "متاسفانه نمیفهمم چی میگی. همونطور که چپ هرگز نفهمید."

# ---------------------- COMMANDS ----------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من بات هوشمندم 🤖")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("کافیه بگی: آب و هوای تهران 🌍")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        city = " ".join(context.args)
        reply = await get_weather(city)
    else:
        reply = "بگو: /weather [اسم شهر]"
    await update.message.reply_text(reply)

# ---------------------- MESSAGES ----------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(f"user({update.message.from_user.id}) in {update.message.chat.type}: \"{text}\"")

    response = await handle_response(text)
    await update.message.reply_text(response)

# ---------------------- ERRORS ----------------------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    print("bot is starting...")

    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("weather", weather_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error_handler)

    print("polling...")
    app.run_polling(poll_interval=3)
