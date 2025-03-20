from flask import Flask
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Token dari BotFather
TOKEN = "8193653698:AAFV54q2qE-TBCWeBTE1f1H3q8IZMDNEUrM"
app = Flask(__name__)
# Fungsi untuk menangani perintah /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Halo! Saya adalah bot kepiting. Siap membantu!")

# Fungsi untuk menangani perintah /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Gunakan perintah berikut:\n/start - Mulai bot\n/help - Bantuan")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Tambahkan handler untuk perintah
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # Jalankan bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
    #app.run(debug=True, port=5000)
