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
    chat_id = context.job.kwargs['CHAT_ID']
    await context.bot.send_message(chat_id=chat_id, text=msg)

def setup_jobs(app, CHAT_ID):
    app.job_queue.run_daily(
        morning_message,
        time=time(6, 30),  # حدود 9 صبح تهران (UTC)
        name="morning",
        kwargs={'CHAT_ID': CHAT_ID}
    )
