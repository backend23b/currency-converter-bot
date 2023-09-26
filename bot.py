from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from dotenv import load_dotenv
import handlers
import os

load_dotenv()
TOKEN = os.environ.get("TOKEN")


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', handlers.start))
    dp.add_handler(CallbackQueryHandler(callback=handlers.currency))
    dp.add_handler(MessageHandler(filters=Filters.text, callback=handlers.convert))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
