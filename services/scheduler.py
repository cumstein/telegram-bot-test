from datetime import time
from telegram.ext import ContextTypes
from services.weather import fetch_daily_forecast
from services.hafez import get_random_hafez
from config import CHAT_ID

async def morning_message(context: ContextTypes.DEFAULT_TYPE):
    cities = ["رشت", "شهریار", "تهرانپارس"]
    msg = "درود دوستان، صبح بخیر 🌅\n\nآب‌وهوای امروز:\n"
    for c in cities:
        msg += fetch_daily_forecast(c) + "\n\n"
    poem = get_random_hafez()
    if poem:
       msg += f"✨ حافظ:\n{poem}\n"
    else:
        msg += "✨ حافظ: نتوانستم شعر حافظ را پیدا کنم.\n"
    chat_id = context.job.data['CHAT_ID']
    await context.bot.send_message(chat_id=chat_id, text=msg)

async def noon_message(context: ContextTypes.DEFAULT_TYPE):
    cities = ["رشت", "شهریار", "تهرانپارس"]
    msg = "ظهر بخیر جیگرا ☀️ خسته نباشید!\n\nآب‌وهوای امروز:\n"
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
    # ساعت ۸ صبح (به وقت UTC: 4:30 یا 5:30 بسته به DST ایران)
    app.job_queue.run_daily(
        morning_message,
        time=time(4, 30),  # اگر ساعت ایران ۸:۰۰ باشد و UTC+3:30
        name="morning",
        data={'CHAT_ID': CHAT_ID}
    )
    # ساعت ۱۳ ظهر (به وقت UTC: 8:30 یا 9:30 بسته به DST ایران)
    app.job_queue.run_daily(
        noon_message,
        time=time(8, 30),  # اگر ساعت ایران ۱۳:۰۰ باشد و UTC+3:30
        name="noon",
        data={'CHAT_ID': CHAT_ID}
    )