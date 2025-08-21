from datetime import time
from telegram.ext import ContextTypes
from services.weather import fetch_daily_forecast
from services.hafez import get_random_hafez
import os

CHAT_ID = os.getenv("CHAT_ID")

async def morning_message(context: ContextTypes.DEFAULT_TYPE):
    cities = ["رشت", "شهریار", "تهرانپارس"]
    msg = "درود دوستان، صبح بخیر 🌅\n\nآب‌وهوای امروز:\n"
    for c in cities:
        msg += fetch_daily_forecast(c) + "\n\n"
    poem = get_random_hafez()
    if poem:
        msg += f"✨ حافظ: {poem}\n"
    await context.bot.send_message(CHAT_ID=context.job.CHAT_ID, text=msg)

def setup_jobs(app, target_CHAT_ID):
    app.job_queue.run_daily(
        morning_message,
        time=time(6, 30),  # حدود 9 صبح تهران (UTC)
        name="morning",
        kwargs={'CHAT_ID': target_CHAT_ID}
    )
