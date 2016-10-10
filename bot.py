#!/bin/python
import sys
import time
import telepot
import random
from pprint import pprint


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    content = msg['text']
    print(content_type, chat_type, chat_id)

    options = { 
        -1 : '[-]', 
        0  : '[  ]', 
        1  : '[+]' 
    }

    ladder = {
        8  : 'Legendary',
        7  : 'Epic',
        6  : 'Fantastic',
        5  : 'Superb',
        4  : 'Great',
        3  : 'Good',
        2  : 'Fair',
        1  : 'Average',
        0  : 'Mediocre',
        -1 : 'Poor',
        -2 : 'Terrible'
    }

    if content_type == 'text':
        print(content)
        if content.startswith('/roll'):
            counter = 0
            value = 0

            dice = []

            while counter < 4:
                choice = random.choice(list(options.keys()))
                dice.append(options[choice])
                value += choice
                counter += 1

            if value > -1:
                print('+')

            print(value)

            if value < -2:
                print('Beyond Terrible')
            elif value > 8:
                print('Beyond Legendary')
            else:
                print(ladder[value])

            pprint(msg)

            bot.sendMessage(
                chat_id, msg['chat']['username'] + ' rolled: ' + ', '.join(dice)
                + ' = ' + str(value)
            )

TOKEN = sys.argv[1] # get token from command line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening...')

# Keep the program running
while 1:
    time.sleep(10)
