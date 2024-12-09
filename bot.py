import subprocess
import logging

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def interact_with_ollama(user_message: str) -> str:
    """Function to interact with the Ollama CLI and get a response."""
    try:
        # Running ollama with the user input
        logger.info(f"Sending message to Meta LLM via CLI: {user_message}")
        process = subprocess.run(
            ["ollama", "run", "llama2"],  # Make sure 'llama3.2' is correct for your setup
            input=user_message,
            text=True,
            capture_output=True,
            check=True
        )
        ai_response = process.stdout.strip()  # Clean the output
        return ai_response
    except subprocess.CalledProcessError as e:
        logger.error(f"Error generating response: {e}")
        return "Sorry, I couldn't process that. Please try again."
