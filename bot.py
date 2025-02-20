from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
from dotenv import load_dotenv
from main import search_for_appointment


# .env dosyasını yükle
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# /start komutunu işleyen fonksiyon
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Bot çalışıyor!")



async def appointment(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    # check_discount fonksiyonunu çağır
    appointment_update_messages = search_for_appointment()

    # Her ürün için ayrı bir mesaj gönder
    for message in appointment_update_messages:
        await context.bot.send_message(chat_id=chat_id, text=message)

# Gelen mesajlara cevap veren fonksiyon
async def echo(update: Update, context: CallbackContext):
    text = update.message.text
    await update.message.reply_text(f"You: {text}")




# Ana fonksiyon
def main():
    app = Application.builder().token(TOKEN).build()

    # Komutları ekleyelim
    app.add_handler(CommandHandler("start", start))  # /start komutu güncellendi
    app.add_handler(CommandHandler("randevu", appointment))  # /product komutu ekli
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
