import os
import time
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Bot token
BOT_TOKEN = "8605916973:AAEnd7M2_Xih_TM1xbGuXIWxusG3CXBuhig"

# Flask app (Railway uchun kerak)
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
    print(f"Start komandasi keldi: {user.first_name}")
    await update.message.reply_text(
        f"👋 Salom, {user.first_name}!\n\n"
        f"Bot ishlayapti ✅\n\n"
        f"Komandalar:\n"
        f"/id - ID olish"
    )

# /id komandasi
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"ID so'raldi: {user.id}")
    await update.message.reply_text(
        f"🆔 Sizning ID: <code>{user.id}</code>", 
        parse_mode='HTML'
    )

def run_bot():
    """Telegram botni ishga tushirish"""
    try:
        print("🤖 Bot ishga tushyapti...")
        
        # Bot yaratish
        app_bot = Application.builder().token(BOT_TOKEN).build()
        
        # Handlerlar
        app_bot.add_handler(CommandHandler("start", start))
        app_bot.add_handler(CommandHandler("id", get_id))
        
        print("✅ Bot ishga tushdi! Xabarlarni kutyapti...")
        
        # Polling
        app_bot.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        print(f"❌ Bot xatosi: {e}")

def run_flask():
    """Flask serverni ishga tushirish"""
    try:
        port = int(os.environ.get("PORT", 8080))
        print(f"🚀 Flask {port} portda ishga tushyapti...")
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        print(f"❌ Flask xatosi: {e}")

if __name__ == "__main__":
    print("🟢 Dastur boshlandi")
    
    # Flask thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Flask ishga tushishi uchun biroz kutish
    time.sleep(2)
    
    # Botni ishga tushirish
    run_bot()
