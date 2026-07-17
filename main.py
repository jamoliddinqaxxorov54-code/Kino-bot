import telebot
import json
import os

TOKEN = "8209686139:AAGTrB0BJAcLDdoslXghDY7hMfEUNiCNkig"
bot = telebot.TeleBot(TOKEN)
DB_FILE = "kinolar.json"

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        kinolar = json.load(f)
else:
    kinolar = {}

kutayotgan_kino = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Salom! Kino kodini yuboring.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    kutayotgan_kino[message.chat.id] = message.video.file_id
    bot.send_message(message.chat.id, "Kino qabul qilindi! Kodini yuboring:")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()
    if chat_id in kutayotgan_kino:
        kinolar[text] = kutayotgan_kino[chat_id]
        with open(DB_FILE, "w") as f:
            json.dump(kinolar, f)
        del kutayotgan_kino[chat_id]
        bot.send_message(chat_id, "✅ Saqlandi!")
    elif text in kinolar:
        bot.send_video(chat_id, kinolar[text])
    else:
        bot.send_message(chat_id, "Topilmadi.")

bot.infinity_polling()

