
import os
import threading

from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)


@app.route("/")
def home():
    return "Synqra Bot is running!"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to Synqra!\n\n"
        "Smart Telegram Automation ⚡\n\n"
        "Fast • Smart • Reliable\n\n"
        "Use /help to see available commands."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Synqra Commands\n\n"
        "/start — Start Synqra\n"
        "/help — Show help\n\n"
        "More automation features coming soon 🚀"
    )


def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is not set")

    threading.Thread(target=run_web, daemon=True).start()

    bot_app = Application.builder().token(TOKEN).build()

    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("help", help_command))

    print("Synqra bot is running...")
    bot_app.run_polling()


if __name__ == "__main__":
    main()
