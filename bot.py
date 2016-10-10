#!/bin/python
import sys
import time
import telepot

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    content = msg['text']
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        print(content)
        if content.startswith('/roll'):
            bot.sendMessage(chat_id, 'Rolling the dice . . .')

TOKEN = sys.argv[1] # get token from command line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening...')

# Keep the program running
while 1:
    time.sleep(10)
