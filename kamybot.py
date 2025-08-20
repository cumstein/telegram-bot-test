import requests
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ---------------- CONFIG ----------------
TOKEN: Final = "8484374008:AAEsLWQjjx5GSoGs-myLtMNJTHqXtsV0wVI"
BOT_USERNAME: Final = "@cumsteinbot"
OPENWEATHER_API_KEY: Final = "f539dc11a658e6e09da2657a4c1acf0d"
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"

# ---------------- STATE ----------------
user_state = {}

# ---------------- COMMANDS ----------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("درود؛ در خدمتم")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "در این مرحله صرفا میتونم بگم:\n"
        "چپ هرگز نفهمید 👀\n"
        "به درود و چطوری هم جواب میدم.\n"
        "فیچر جدید: آب و هوا 🌤"
    )

async def chap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("چپ هرگز نفهمید!")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_state[user_id] = "waiting_for_city"
    await update.message.reply_text("اسم شهر مورد نظر رو بگو 🏙")

# ---------------- WEATHER FUNCS ----------------
def get_city_coordinates(city_name: str):
    try:
        params = {
            "q": city_name,
            "format": "json",
            "accept-language": "fa"
        }
        headers = {
            "User-Agent": "TelegramWeatherBot/1.0 (kamstein@gmail.com)"
        }
        response = requests.get(GEOCODE_URL, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            print("Geocode API Error:", response.status_code, response.text[:100])
            return None

        data = response.json()
        if not data:
            return None
        return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]

    except Exception as e:
        print("Error in get_city_coordinates:", e)
        return None

def get_weather(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=fa"
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        print("Error in get_weather:", e)
        return None

# ---------------- RESPONSES ----------------
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "درود" in processed:
        return "درود عمویی"
    if "چطوری" in processed:
        return "مخلصم"
    if "سلام" in processed:
        return "سلام رو نمیفهمم باید بگی درود"
    if "چپ" in processed:
        return "چپ هرگز نفهمید!"
    if "آب و هوا" in processed:
        return "بگو اسم شهری که میخوای 🌍"
    return "متاسفانه نمیفهمم چی میگی. همونطور که چپ هرگز نفهمید."

# ---------------- MESSAGES ----------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text: str = update.message.text
    user_id = update.message.from_user.id

    print(f'user({update.message.chat.id}) in {message_type}: "{text}"')

    # --- حالت انتظار شهر ---
    if user_id in user_state and user_state[user_id] == "waiting_for_city":
        coords = get_city_coordinates(text)
        if coords:
            lat, lon, display_name = coords
            weather_data = get_weather(lat, lon)
            if weather_data and "main" in weather_data:
                temp = weather_data["main"]["temp"]
                desc = weather_data["weather"][0]["description"]
                await update.message.reply_text(
                    f"آب و هوای {display_name}:\n{desc}, دما: {temp}°C 🌡"
                )
            else:
                await update.message.reply_text("نتونستم وضعیت هوا رو بگیرم 😞")
        else:
            await update.message.reply_text("اسم شهر درست نبود یا پیدا نشد 🚫")

        user_state.pop(user_id, None)
        return

    # --- گروه و سوپرگروه ---
    if message_type in ["group", "supergroup"]:
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        elif "چپ" in text:
            response: str = handle_response("چپ هرگز نفهمید")
        else:
            return
    else:
        response: str = handle_response(text)

    print("bot:", response)
    await update.message.reply_text(response)

# ---------------- ERRORS ----------------
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error : {context.error}")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("bot is starting...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("chap", chap_command))
    app.add_handler(CommandHandler("weather", weather_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    print("polling...")
    app.run_polling(poll_interval=3)