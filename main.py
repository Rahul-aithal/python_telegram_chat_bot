import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from bot import interact_with_ollama  # Import function from bot.py

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")  # Ensure your Telegram Bot token is set in the .env file

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm your AI chatbot powered by Meta LLM (via Ollama CLI). How can I assist you today?")

# Define the text message handler
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    try:
        # Use the function from bot.py to interact with Ollama CLI
        ai_response = interact_with_ollama(user_message)
        await update.message.reply_text(ai_response)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await update.message.reply_text("Sorry, I couldn't process that. Please try again.")

def main():
    # Build the application
    app = ApplicationBuilder().token(TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Start the bot
    logger.info("Starting Telegram bot...")
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
