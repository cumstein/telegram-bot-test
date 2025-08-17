from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = "8484374008:AAEsLWQjjx5GSoGs-myLtMNJTHqXtsV0wVI"
BOT_USERNAME: Final = "@cumsteinbot"

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("درود؛ در خدمتم")
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("در این مرحله صرفا میتونم بگم چپ هرگز نفهمید. اگرچه ممکن است به روز رسانی شوم. عجالتا چپ هرگز نفهمید. به درود و چطوری هم پاسخ میدم")

async def chap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("چپ هرگز نفهمید!")

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
    return "متاسفانه نمیفهمم چی میگی. همونطور که چپ هرگز نفهمید."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text: str = update.message.text
    print(f'user({update.message.chat.id}) in {message_type}: "{text}"')
    
    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
            
        elif "چپ" in text:
            response: str = handle_response("چپ هرگز نفهمید")
        else: 
            return
    else:
        response: str = handle_response(text)

#supergroup
    if message_type == "supergroup":
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
    

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error : {context.error}")

if __name__ == "__main__":
    print("bot is starting...")
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("chap", chap_command))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    # Polling
    print("polling...")
    app.run_polling(poll_interval=3)