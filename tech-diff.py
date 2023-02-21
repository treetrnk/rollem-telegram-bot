import sys
import logging
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# CONFIGURATION

TOKEN = sys.argv[1]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# HANDLERS

def warning(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Estamos com problemas técnicos no momento. Tente novamente mais tarde.")

# MAIN
if __name__ == '__main__':
    app = ApplicationBuilder(TOKEN)
    app.add_handler(CommandHandler(['start', 'help', 'roll', 'r', 'rf'], warning, context_types=ContextTypes.ALL))
    app.run()
