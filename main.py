import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Bot token
BOT_TOKEN = "8605916973:AAEnd7M2_Xih_TM1xbGuXIWxusG3CXBuhig"

# Flask app (Railway uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti! ✅"

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"Start komandasi keldi: {user.first_name}")
    await update.message.reply_text(
        f"👋 Assalomu alaykum, {user.first_name}!\n\n"
        f"Bot ishga tushdi! ✅\n\n"
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

# Barcha xabarlarni ushlash (test uchun)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    print(f"Xabar keldi: {text} - {user.first_name}")
    await update.message.reply_text(f"Siz yozdingiz: {text}")

def run_bot():
    """Botni ishga tushirish"""
    try:
        print("Bot ishga tushyapti...")
        
        # Botni yaratish
        app_bot = Application.builder().token(BOT_TOKEN).build()
        
        # Handlerlarni qo'shish
        app_bot.add_handler(CommandHandler("start", start))
        app_bot.add_handler(CommandHandler("id", get_id))
        
        # TEST: Barcha xabarlarga javob berish
        app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        print("✅ Bot ishga tushdi! Xabarlarni kutyapti...")
        
        # Pollingni boshlash
        app_bot.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        print(f"❌ Bot xatosi: {e}")

def run_flask():
    """Flask serverni ishga tushirish"""
    try:
        port = int(os.environ.get("PORT", 8080))
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        print(f"Flask xatosi: {e}")

if __name__ == "__main__":
    print("🟢 Dastur ishga tushyapti...")
    
    # Flask ni alohida threadda ishga tushirish
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Botni ishga tushirish (asosiy thread)
    run_bot()
