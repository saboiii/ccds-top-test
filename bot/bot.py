import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from pymongo import MongoClient

# used some chatgpt and documentation here, so idk if this is how the bot is usually set up

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)

client = MongoClient(MONGODB_URI) 
db = client["telegram_bot"] 
messages_collection = db["messages"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.full_name
    user_message = "gang wuss good"
    
    logging.info(f"start command from {user_name}")
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=user_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.full_name
    user_message = update.message.text
    timestamp = datetime.utcnow() 
    
    logging.info(f"message from {user_name}: {user_message}")
    
    message_data = {
        "user_name": user_name,
        "user_message": user_message,
        "timestamp": timestamp
    }
    messages_collection.insert_one(message_data)
    logging.info(f"message stored from {user_name} at {timestamp}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"i got this message: {user_message}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)

    application.run_polling()
