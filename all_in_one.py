import os
import sqlite3
import threading
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# =====================================
# CONFIG
# =====================================
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PORT = 5000

# =====================================
# DATABASE
# =====================================

db = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

db.commit()

print("✅ Database Ready")

# =====================================
# FLASK APP
# =====================================

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# =====================================
# WEBSITE
# =====================================

@app.route("/")
def home():

    return """
    <html>

    <head>

    <title>All In One Dashboard</title>

    <style>

    body{
        background:#111;
        color:white;
        font-family:Arial;
        text-align:center;
        padding:30px;
    }

    .card{
        background:#222;
        padding:20px;
        margin:20px;
        border-radius:12px;
    }

    </style>

    </head>

    <body>

    <h1>🚀 ALL IN ONE SYSTEM</h1>

    <div class="card">
    <h2>🤖 Telegram Bot Running</h2>
    </div>

    <div class="card">
    <h2>🌐 Flask Server Online</h2>
    </div>

    <div class="card">
    <h2>🗄️ Database Connected</h2>
    </div>

    </body>
    </html>
    """

# =====================================
# STATUS API
# =====================================

@app.route("/status")
def status():

    return jsonify({
        "server": "online",
        "telegram": "running"
    })

# =====================================
# REGISTER API
# =====================================

@app.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    cursor.execute(
        "INSERT INTO users(username,password) VALUES(?,?)",
        (username, password)
    )

    db.commit()

    return jsonify({
        "status": "registered"
    })

# =====================================
# LOGIN API
# =====================================

@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    if user:

        return jsonify({
            "status": "success"
        })

    return jsonify({
        "status": "failed"
    })

# =====================================
# FILE UPLOAD
# =====================================

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(path)

    return jsonify({
        "uploaded": file.filename
    })

# =====================================
# WEBHOOK
# =====================================

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    send_notification(
        f"📩 Webhook:\n{data}"
    )

    return jsonify({
        "status": "received"
    })

# =====================================
# TELEGRAM NOTIFICATION
# =====================================

def send_notification(text):

    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendMessage"
    )

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

# =====================================
# TELEGRAM BOT COMMANDS
# =====================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🚀 All In One Bot Running!"
    )

# =====================================

async def calc(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        a = int(context.args[0])
        b = int(context.args[1])

        result = a + b

        await update.message.reply_text(
            f"🧮 Result = {result}"
        )

    except:

        await update.message.reply_text(
            "Usage: /calc 5 10"
        )

# =====================================

async def ai(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = " ".join(context.args)

    if not text:

        await update.message.reply_text(
            "Usage: /ai hello"
        )

        return

    reply = f"🤖 You said: {text}"

    await update.message.reply_text(reply)

# =====================================

async def send_file(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    with open("hello.txt", "w") as f:

        f.write("Hello from bot!")

    await update.message.reply_document(
        document=open("hello.txt", "rb")
    )

# =====================================
# FOLDER MONITOR
# =====================================

def monitor():

    folder = "monitor"

    os.makedirs(folder, exist_ok=True)

    old_files = os.listdir(folder)

    while True:

        new_files = os.listdir(folder)

        if new_files != old_files:

            print("⚠️ Folder Changed")

            send_notification(
                "⚠️ Folder changed detected"
            )

            old_files = new_files

# =====================================
# RUN TELEGRAM BOT
# =====================================

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
        CommandHandler("calc", calc)
    )

    bot.add_handler(
        CommandHandler("ai", ai)
    )

    bot.add_handler(
        CommandHandler("file", send_file)
    )

    print("🤖 Telegram Bot Running")

    bot.run_polling()

# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    threading.Thread(
        target=run_bot
    ).start()

    threading.Thread(
        target=monitor
    ).start()

    print("🌐 Flask Running")

    app.run(
        host="0.0.0.0",
        port=PORT
    )
