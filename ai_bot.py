import os
import sqlite3
import requests
from dotenv import load_dotenv
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# =========================
# CONFIG
# =========================
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# =========================
# DATABASE
# =========================

db = sqlite3.connect(
    "bot.db",
    check_same_thread=False
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username TEXT
)
""")

db.commit()

print("✅ Database Ready")

# =========================
# FLASK DASHBOARD
# =========================

app = Flask(__name__)

@app.route("/")
def home():

    return """
    <h1>🚀 AI Telegram Bot</h1>
    <p>Server Running ✅</p>
    """

# =========================
# AI REPLY
# =========================

def ai_reply(text):

    # Simple AI logic

    text = text.lower()

    if "hello" in text:
        return "👋 Hello!"

    if "hi" in text:
        return "🤖 Hi there!"

    if "how are you" in text:
        return "😄 I'm good!"

    return f"🤖 You said: {text}"

# =========================
# START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    cursor.execute(
        "INSERT OR IGNORE INTO users(id,username) VALUES(?,?)",
        (user.id, user.username)
    )

    db.commit()

    await update.message.reply_text(
        f"""
🚀 AI BOT ACTIVE

👤 User:
{user.first_name}

🆔:
{user.id}

✅ System Online
"""
    )

# =========================
# HELP
# =========================

async def help_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
"""
📚 COMMANDS

/start
/help
/users
/broadcast
/ping
"""
    )

# =========================
# USERS
# =========================

async def users(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:
        return

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    total = cursor.fetchone()[0]

    await update.message.reply_text(
        f"👥 Total Users: {total}"
    )

# =========================
# BROADCAST
# =========================

async def broadcast(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:
        return

    msg = " ".join(context.args)

    cursor.execute(
        "SELECT id FROM users"
    )

    users = cursor.fetchall()

    success = 0

    for user in users:

        try:

            await context.bot.send_message(
                chat_id=user[0],
                text=msg
            )

            success += 1

        except:
            pass

    await update.message.reply_text(
        f"✅ Sent to {success} users"
    )

# =========================
# PING
# =========================

async def ping(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🏓 Pong!"
    )

# =========================
# FILE HANDLER
# =========================

async def file_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    document = update.message.document

    if not document:
        return

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file = await context.bot.get_file(
        document.file_id
    )

    path = (
        f"uploads/{document.file_name}"
    )

    await file.download_to_drive(path)

    await update.message.reply_text(
        f"✅ File Saved:\n{path}"
    )

# =========================
# AI CHAT
# =========================

async def chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    reply = ai_reply(text)

    await update.message.reply_text(
        reply
    )

# =========================
# RUN BOT
# =========================

def run_bot():

    bot = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    bot.add_handler(
        CommandHandler("start", start)
    )

    bot.add_handler(
        CommandHandler("help", help_cmd)
    )

    bot.add_handler(
        CommandHandler("users", users)
    )

    bot.add_handler(
        CommandHandler("broadcast", broadcast)
    )

    bot.add_handler(
        CommandHandler("ping", ping)
    )

    bot.add_handler(
        MessageHandler(
            filters.Document.ALL,
            file_handler
        )
    )

    bot.add_handler(
        MessageHandler(
            filters.TEXT,
            chat
        )
    )

    print("🤖 BOT RUNNING")

    bot.run_polling(
        stop_signals=None
    )

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    import threading

    threading.Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=5000,
            debug=False,
            use_reloader=False
        ),
        daemon=True
    ).start()

    run_bot()
