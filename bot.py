import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")


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


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is not set")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("Synqra bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
