import subprocess
import logging
import csv
from transformers import pipeline

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# File to store sentiment analysis logs
SENTIMENT_CSV = "sentiment_analysis.csv"

# Initialize the CSV file with headers (if not exists)
def initialize_csv():
    try:
        with open(SENTIMENT_CSV, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Message", "Sentiment", "Confidence"])
    except Exception as e:
        logger.error(f"Error initializing CSV file: {e}")

# Perform sentiment analysis and log it
def analyze_sentiment(text: str) -> dict:
    """Perform sentiment analysis on the given text and return the result."""
    try:
        sentiment_result = sentiment_analyzer(text)[0]  # Analyze text
        sentiment = sentiment_result['label']
        confidence = sentiment_result['score']
        
        # Log sentiment to CSV
        with open(SENTIMENT_CSV, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([text, sentiment, confidence])
        
        logger.info(f"Sentiment logged: {text} -> {sentiment} (Confidence: {confidence:.2f})")
        return {"sentiment": sentiment, "confidence": confidence}
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        return {"sentiment": "Unknown", "confidence": 0.0}

# Interact with the Ollama CLI
def interact_with_ollama(user_message: str) -> str:
    """Function to interact with the Ollama CLI and get a response."""
    try:
        # Running Ollama with the user input
        logger.info(f"Sending message to Meta LLM via CLI: {user_message}")
        process = subprocess.run(
            ["ollama", "run", "llama3.2"],  # Adjust "llama2" based on your Ollama model
            input=user_message,
            text=True,
            capture_output=True,
            check=True
        )
        ai_response = process.stdout.strip()  # Clean the output
        logger.info(f"AI Response: {ai_response}")
        return ai_response
    except subprocess.CalledProcessError as e:
        logger.error(f"Error generating response: {e}")
        return "Sorry, I couldn't process that. Please try again."

# Combined function for Chat and Sentiment
def chat_and_analyze(user_message: str) -> str:
    """Handle user input, generate AI response, and analyze sentiments."""
    # Analyze sentiment of the user's message
    user_sentiment = analyze_sentiment(user_message)
    # Get AI response via Ollama CLI
    ai_response = interact_with_ollama(user_message)

    # Analyze sentiment of the AI's response
    ai_sentiment = analyze_sentiment(ai_response)

    # Log results for debugging (Optional)
    logger.info(f"User Sentiment: {user_sentiment}")
    logger.info(f"AI Sentiment: {ai_sentiment}")

    # Return a combined response
    combined_response = (
        f"**User Sentiment:** {user_sentiment['sentiment']} (Confidence: {user_sentiment['confidence']:.2f})\n"
        f"**AI Response:** {ai_response}\n"
        f"**AI Sentiment:** {ai_sentiment['sentiment']} (Confidence: {ai_sentiment['confidence']:.2f})"
    )
    return combined_response
