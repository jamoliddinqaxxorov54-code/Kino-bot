import telebot
import json
import os
import threading
from flask import Flask

# 1. BOT TOKENINGIZNI SHU YERGA YOZING
TOKEN = "8209686139:AAGTrB0BJAcLDdoslXghDY7hMfEUNiCNkig"


bot = telebot.TeleBot(TOKEN)
DB_FILE = "kinolar.json"

# Kinolar bazasini yuklash
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        kinolar = json.load(f)
else:
    kinolar = {}

# Vaqtinchalik yuklangan kinoni saqlab turish uchun
kutayotgan_kino = {}

# Flask serverini yaratish
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti!"

# Botga /start bosilganda
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, 
        "Salom! Kino kodini yuboring, men uni topib beraman! 🍿\n\n"
        "*(Admin bo'lsangiz, shunchaki kino yuboring)*"
    )

# Admin kino (video) yuborganda
@bot.message_handler(content_types=['video'])
def handle_video(message):
    chat_id = message.chat.id
    video_id = message.video.file_id
    
    kutayotgan_kino[chat_id] = video_id
    bot.send_message(chat_id, "Kino qabul qilindi! Endi ushbu kino uchun kod (son) yuboring:")

# Matnli xabarlar kelganda
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id in kutayotgan_kino:
        video_id = kutayotgan_kino[chat_id]
        kinolar[text] = video_id
        with open(DB_FILE, "w") as f:
            json.dump(kinolar, f)
        del kutayotgan_kino[chat_id]
        bot.send_message(chat_id, f"✅ Muvaffaqiyatli saqlandi! Kino kodi: {text}")
        return

    if text in kinolar:
        bot.send_video(chat_id, kinolar[text], caption=f"🎬 Kino kodi: {text}\nYoqimli tomosha!")
    else:
        bot.send_message(chat_id, "😔 Afsuski, bunday kod bilan kino topilmadi.")

# Botni va Flaskni ishga tushirish
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
