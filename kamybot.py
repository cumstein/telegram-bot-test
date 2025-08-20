import requests
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = "8484374008:AAEsLWQjjx5GSoGs-myLtMNJTHqXtsV0wVI"
BOT_USERNAME: Final = "@cumsteinbot"
OPENWEATHER_API_KEY: Final = "f539dc11a658e6e09da2657a4c1acf0d"
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"

user_state = {}

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("درود؛ در خدمتم")
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("در این مرحله صرفا میتونم بگم چپ هرگز نفهمید. اگرچه ممکن است به روز رسانی شوم. عجالتا چپ هرگز نفهمید. به درود و چطوری هم پاسخ میدم. فیچر جدید آب و هوا هم اضافه کردم")

async def chap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("چپ هرگز نفهمید!")
    
async def weather_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_state[user_id] = "waiting_for_city"
    await update.message.reply_text("اسم شهر مورد نظر رو بگو")

# weather functions (همونایی که خودت داشتی)
def get_city_coordinates(city_name:str):
    params = {"q": city_name, "format": "json", "accept_language":"fa"}
    response = requests.get(GEOCODE_URL, params=params)
    data = response.json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]

def get_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=fa"
    response = requests.get(url)
    return response.json()

# responses
def handle_response(text: str ) -> str:
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
        return "اسم شهر مورد نظر رو بگو"
    return "متاسفانه نمیفهمم چی میگی. همونطور که چپ هرگز نفهمید."

# پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text: str = update.message.text
    user_id = update.message.from_user.id
    print(f'user({update.message.chat.id}) in {message_type}: "{text}"')

    # اگر منتظر اسم شهر هستیم، همینجا هندل کن و برگرد
    if user_state.get(user_id) == "waiting_for_city":
        city_name = text.strip()
        coords = get_city_coordinates(city_name)
        if not coords:
            await update.message.reply_text("شهر پیدا نشد ❌ دوباره اسم شهر رو بگو")
            return  # در همین حالت می‌مانیم تا دوباره اسم شهر بده
        lat, lon, display_name = coords
        w = get_weather(lat, lon)
        if "main" in w:
            temp = w["main"]["temp"]
            desc = w["weather"][0]["description"]
            await update.message.reply_text(f"آب و هوای {display_name}:\n🌡 دما: {temp}°C\n🌤 وضعیت: {desc}")
        else:
            await update.message.reply_text("نتونستم اطلاعات آب‌وهوا رو بگیرم 😕")
        user_state[user_id] = None
        return

    # حالت نرمال: مثل قبل + تشخیص «آب و هوا»
    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
            used_text = new_text
        elif "چپ" in text or "آب و هوا" in text:
            response: str = handle_response(text)
            used_text = text
        else: 
            return
    else:
        response: str = handle_response(text)
        used_text = text
    # supergroup (مطابق الگوی خودت)
    if message_type == "supergroup":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
            used_text = new_text
        elif "چپ" in text or "آب و هوا" in text:
            response: str = handle_response(text)
            used_text = text
        else: 
            return
    else:
        # در چت‌های غیر سوپرگروپ از بالایی استفاده می‌کنیم
        pass

    print("bot:", response)
    await update.message.reply_text(response)

    # اگر «آب و هوا» گفته شد، وارد حالت انتظار اسم شهر شو
    if "آب و هوا" in used_text:
        user_state[user_id] = "waiting_for_city"
    

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error : {context.error}")

if __name__ == "__main__":
    print("bot is starting...")
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("chap", chap_command))
    app.add_handler(CommandHandler("weather", weather_command))  # اختیاری: کامند مستقیم آب‌وهوا

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    # Polling
    print("polling...")
    app.run_polling(poll_interval=3)