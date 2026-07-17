import telebot
import json
import os

# 1. BOT TOKENINGIZNI SHU YERGA YOZING
TOKEN = "Sizning_Bot_Tokeningiz_Shu_Yurga_Yoziladi" 

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

# Matnli xabarlar kelganda (Kod kiritilganda yoki izlanganda)
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()

    # Agar admin kino yuklagan bo'lsa va kodini yozgan bo'lsa
    if chat_id in kutayotgan_kino:
        video_id = kutayotgan_kino[chat_id]
        kinolar[text] = video_id
        
        with open(DB_FILE, "w") as f:
            json.dump(kinolar, f)
            
        del kutayotgan_kino[chat_id]
        bot.send_message(chat_id, f"✅ Muvaffaqiyatli saqlandi! Kino kodi: {text}")
        return

    # Agar foydalanuvchi kino qidirayotgan bo'lsa
    if text in kinolar:
        bot.send_video(chat_id, kinolar[text], caption=f"🎬 Kino kodi: {text}\nYoqimli tomosha!")
    else:
        bot.send_message(chat_id, "😔 Afsuski, bunday kod bilan kino topilmadi. Kodni to'g'ri yozganingizni tekshiring.")

# Botni uzluksiz ishlatish
bot.polling(none_stop=True)
