# Python Telegram Chat Bot

A simple Telegram chatbot that uses [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) and calls a local Ollama model to generate replies.

## Features

- `/start` command greeting
- Handles normal text messages from users
- Sends prompts to `ollama run llama2`
- Returns model responses back to Telegram chat

## Requirements

- Python 3.10+
- A Telegram bot token
- Ollama installed and available in your PATH
- A pulled Ollama model (default in this project: `llama2`)

## Setup

1. Clone the repository and move into it.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```env
   TOKEN=your_telegram_bot_token_here
   ```

4. Make sure Ollama is installed and the model exists:

   ```bash
   ollama pull llama2
   ```

## Run

Start the bot:

```bash
python main.py
```

You should see:

```text
Bot is running...
```

## Project Structure

- `main.py` – Telegram bot setup, handlers, and polling loop
- `bot.py` – function that invokes Ollama CLI and returns responses
- `requirements.txt` – Python dependencies

## Notes

- If `TOKEN` is missing or invalid, the bot will fail to start.
- If Ollama is not installed/running, message generation will fail and the bot will return an error message.
