from telegram import Update
from telegram.ext import ContextTypes
from config import pending_city_request
from services.weather import fetch_weather
from services.scheduler import send_daily_message

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
async def test_daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_daily_message(context.bot)