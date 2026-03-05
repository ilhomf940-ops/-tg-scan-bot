import os
import sys
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Bot token
BOT_TOKEN = "8605916973:AAEnd7M2_Xih_TM1xbGuXIWxusG3CXBuhig"

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti! ✅"

@app.route('/health')
def health():
    return "OK", 200

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"👋 Salom, {user.first_name}!\n\nBot ishlayapti ✅")

# /id komandasi
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"🆔 ID: {user.id}")

def run_bot():
    """Botni ishga tushirish"""
    try:
        print("🤖 Bot ishga tushyapti...")
        app_bot = Application.builder().token(BOT_TOKEN).build()
        app_bot.add_handler(CommandHandler("start", start))
        app_bot.add_handler(CommandHandler("id", get_id))
        print("✅ Bot ishga tushdi!")
        app_bot.run_polling()
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        sys.exit(1)

def run_flask():
    """Flask serverni ishga tushirish"""
    try:
        port = int(os.environ.get("PORT", 8080))
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        print(f"Flask xatosi: {e}")

if __name__ == "__main__":
    print("🚀 Dastur ishga tushdi")
    
    # Flask thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Bot
    run_bot()
