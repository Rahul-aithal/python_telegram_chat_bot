import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from bot import interact_with_ollama, analyze_sentiment  # Import functions from bot.py
from dotenv import load_dotenv
import os
from google_search import google_search_with_curl

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")  # Ensure your Telegram Bot token is set in the .env file

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message to the user when they use the /start command."""
    await update.message.reply_text("Hello! I'm your AI chatbot. How can I assist you today?")

# Define the text message handler
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages: Generate AI response and analyze sentiment separately."""
    user_message = update.message.text
    try:
        # Interact with Ollama to generate AI response
        ai_response = interact_with_ollama(user_message)

        # Perform sentiment analysis on the user message
        user_sentiment = analyze_sentiment(user_message)

        # Perform sentiment analysis on the AI response
        ai_sentiment = analyze_sentiment(ai_response)
        
        # Reply with AI response and individual sentiment results
        await update.message.reply_text(
            f"\n{ai_response}\n"

        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await update.message.reply_text("Sorry, I couldn't process that. Please try again.")

# Define the /search command handler to search on Google using curl
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Search Google and return the top result."""
    query = " ".join(context.args)  # Get the query from the command arguments
    if not query:
        await update.message.reply_text("Please provide a search query. Example: /search Python programming")
        return
    try:
        response = google_search_with_curl(query)
        print(analyze_sentiment(response))
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error during search: {e}")
        await update.message.reply_text("Sorry, I couldn't fetch search results. Please try again.")

def main():
    """Main function to run the Telegram bot."""
    # Build the application
    app = ApplicationBuilder().token(TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))  # Add /search handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Start the bot
    logger.info("Starting Telegram bot...")
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
