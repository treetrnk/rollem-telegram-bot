#! /home/nathan/.virtualenvs/rollem/bin/python
import sys
import logging
from telegram.ext import Updater, CommandHandler

def roll(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Technical difficulties. Working on a fix now!")

TOKEN = sys.argv[1]

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

roll_handler = CommandHandler('roll', roll)
dispatcher.add_handler(roll_handler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
         level=logging.INFO)

updater.start_polling()
