from telegram import Update
from telegram.ext import ContextTypes

async def log_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    chat_title = update.effective_chat.title or update.effective_chat.username
    print(f"[LOGGER] Chat ID: {chat_id}, Type: {chat_type}, Title: {chat_title}")

    await update.message.reply_text(f"Chat ID شما: {chat_id}")
