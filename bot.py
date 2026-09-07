import os
import threading
import logging

from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


# ==============================
# CONFIG
# ==============================

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")


# ==============================
# LOGGING
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("Synqra")


# ==============================
# RENDER WEB SERVER
# ==============================

app = Flask(__name__)


@app.route("/")
def home():
    return "Synqra Bot is running! 🤖"


@app.route("/health")
def health():
    return "OK"


def run_web():
    port = int(os.getenv("PORT", "10000"))

    app.run(
        host="0.0.0.0",
        port=port
    )


# ==============================
# AUTO REPLIES
# ==============================

auto_replies = {
    "hi": "👋 Hello! Welcome to Synqra.",
    "hello": "🤖 Hello! Synqra is ready to help you.",
    "hey": "⚡ Hey! Synqra is online.",
    "good morning": "🌅 Good morning! Have a productive day.",
    "thanks": "😊 You're welcome!",
}


# ==============================
# START
# ==============================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🤖 Welcome to Synqra!\n\n"
        "⚡ Smart Telegram Automation\n"
        "🚀 Fast • Simple • Reliable\n\n"
        "Use /help to see available commands."
    )


# ==============================
# HELP
# ==============================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🛠 Synqra Commands\n\n"
        "/start — Start Synqra\n"
        "/help — Show commands\n"
        "/setreply keyword | reply — Add auto reply\n"
        "/delreply keyword — Delete auto reply\n"
        "/replies — Show auto replies\n\n"
        "💬 Send a message containing a saved "
        "keyword and Synqra will reply automatically."
    )


# ==============================
# SET REPLY
# ==============================

async def set_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text or ""

    if "|" not in text:

        await update.message.reply_text(
            "❌ Wrong format.\n\n"
            "Use:\n"
            "/setreply hello | Hello! 👋"
        )

        return

    keyword, reply = text.split("|", 1)

    keyword = keyword.replace(
        "/setreply",
        "",
        1
    ).strip().lower()

    reply = reply.strip()

    if not keyword or not reply:

        await update.message.reply_text(
            "❌ Keyword and reply cannot be empty."
        )

        return

    auto_replies[keyword] = reply

    await update.message.reply_text(
        f"✅ Auto reply added!\n\n"
        f"🔑 Keyword: {keyword}\n"
        f"💬 Reply: {reply}"
    )


# ==============================
# DELETE REPLY
# ==============================

async def delete_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text or ""

    keyword = text.replace(
        "/delreply",
        "",
        1
    ).strip().lower()

    if not keyword:

        await update.message.reply_text(
            "❌ Use:\n/delreply hello"
        )

        return

    if keyword in auto_replies:

        del auto_replies[keyword]

        await update.message.reply_text(
            f"🗑 Auto reply deleted for: {keyword}"
        )

    else:

        await update.message.reply_text(
            f"❌ No auto reply found for: {keyword}"
        )


# ==============================
# SHOW REPLIES
# ==============================

async def show_replies(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not auto_replies:

        await update.message.reply_text(
            "📭 No auto replies configured."
        )

        return

    text = "🤖 Synqra Auto Replies\n\n"

    for keyword, reply in auto_replies.items():

        text += (
            f"🔑 {keyword}\n"
            f"💬 {reply}\n\n"
        )

    await update.message.reply_text(text)


# ==============================
# AUTO REPLY
# ==============================

async def auto_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    if not update.message.text:
        return

    message = update.message.text.lower().strip()

    # Exact match first
    if message in auto_replies:

        await update.message.reply_text(
            auto_replies[message]
        )

        return

    # Keyword match
    for keyword, reply in auto_replies.items():

        if keyword in message:

            await update.message.reply_text(
                reply
            )

            return


# ==============================
# ERROR HANDLER
# ==============================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        "Telegram error: %s",
        context.error
    )


# ==============================
# MAIN
# ==============================

def main():

    # Start Render web server
    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    # Create Telegram bot
    bot = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    bot.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    bot.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    bot.add_handler(
        CommandHandler(
            "setreply",
            set_reply
        )
    )

    bot.add_handler(
        CommandHandler(
            "delreply",
            delete_reply
        )
    )

    bot.add_handler(
        CommandHandler(
            "replies",
            show_replies
        )
    )

    # Normal messages
    bot.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            auto_reply
        )
    )

    # Error handler
    bot.add_error_handler(
        error_handler
    )

    logger.info(
        "🚀 Synqra Bot is running..."
    )

    bot.run_polling(
        drop_pending_updates=True
    )


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    main()
