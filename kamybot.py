from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN
from handlers.commands import start_command, help_command, weather_command, chap_command
from handlers.messages import handle_message
from handlers.logger import log_chat_id

if __name__ == "__main__":
    print("bot is starting...")

    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("chap", chap_command))
    app.add_handler(CommandHandler("id", log_chat_id))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("polling...")
    app.run_polling(poll_interval=3)
