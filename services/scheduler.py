from datetime import datetime, timedelta, time
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
    else:
        msg += "✨ حافظ: نتوانستم شعر حافظ را پیدا کنم.\n"
    chat_id = context.job.data['CHAT_ID']
    await context.bot.send_message(chat_id=chat_id, text=msg)

def setup_jobs(app):
    # برای تست: ۲ دقیقه بعد از اجرای بات
    now = datetime.utcnow() + timedelta(minutes=2)
    app.job_queue.run_daily(
        morning_message,
        time=time(now.hour, now.minute),
        name="morning",
        data={'CHAT_ID': CHAT_ID}
    )