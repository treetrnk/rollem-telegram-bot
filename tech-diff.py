#! /home/nathan/.virtualenvs/rollem/bin/python
import sys
import logging
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler

def roll(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Technical difficulties. Working on a fix now!")

def help(bot, update):
    response = ("<b>Rollem Bot - Help</b>\r\n"
        "This bot allows you to roll all kinds of dice in "
        "your Telegram messages. To roll dice, you can use the "
        "<code>/roll</code> or <code>/r</code> commands, followed by "
        "<a href='https://en.wikipedia.org/wiki/Dice_notation'>dice notation</a> "
        "with no spaces in it.\r\n"
        "For example: <code>/r 4d10+3d6</code>\r\n\r\n"
        "<b>Fate Dice</b>\r\n"
        "To roll Fate or Fudge dice, you can use the <code>4dF</code> "
        "notation, or the shorthand command <code>/rf</code>. "
        "Adding a number after the <code>/rf</code> will add it to the "
        "total of the four Fate dice. So <code>/rf 3</code> will roll "
        "4 Fate dice and add 3 to the result.\r\n\r\n"
        "<b>Comments</b>\r\n"
        "You can add comments to the end of a roll by separating it from "
        "the equation with a space, like this: <code>/r 8d6 Fireball!!!"
        "</code>\r\n\r\n"
        "<b>Support</b>\r\n"
        "This bot was created and is worked on in my free time and it is "
        "hosted on a server that I pay for with my own money. If you "
        "would like to say thanks, support further development, or "
        "check out some of my other projects, take a look at the links "
        "below.\r\n"
        " - <a href='https://github.com/treetrnk'>Github</a>\r\n"
        " - <a href='https://rpg.nathanhare.net'>Blog about Fate Core and other RPGs</a>\r\n"
        " - <a href='https://nathanhare.net'>Portfolio</a>\r\n"
        " - <a href='https://www.drivethrurpg.com/browse/pub/10796/Nathan-Hare'>DriveThruRPG Webstore</a>\r\n"
        " - <a href='https://paypal.me/treetrnk'>Paypal</a>"
    )
    bot.send_message(chat_id=update.message.chat_id, text=response, parse_mode=ParseMode.HTML)
    

TOKEN = sys.argv[1]

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

roll_handler = CommandHandler(['roll','rf','r'], roll)
dispatcher.add_handler(roll_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
         level=logging.INFO)

updater.start_polling()
