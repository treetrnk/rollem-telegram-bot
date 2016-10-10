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
        -1 : '[‒]', 
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
        if content.startswith('/roll') or content.startswith('/r'):
            counter = 0
            value = 0

            dice = []

            while counter < 4:
                choice = random.choice(list(options.keys()))
                dice.append(options[choice])
                value += choice
                counter += 1

            print(value)

            msg_list = msg['text'].split()

            if len(msg_list) >= 2:
                try: 
                    if isinstance(eval(msg_list[1]), int):
                        value = str(value) + ' + ' + msg_list[1]
                        labelat = 2
                except NameError:
                    labelat = 1

                if len(msg_list) >= (labelat + 1):
                    msg_begin, keyword, msg_end = msg['text'].partition(msg_list[labelat])
                    action_text = ' ' + keyword + msg_end
                else:
                    action_text = ''


            result = eval(str(value))

            if result > -1:
                sign = '+'
            else:
                sign = ''

            if result < -2:
                ladder_result = 'Beyond Terrible'
            elif result > 8:
                ladder_result = 'Beyond Legendary'
            else:
                ladder_result = ladder[result]

            # === Uncomment for Debugging ===
            # pprint(msg)

            if 'username' in msg['from'].keys():
                user = msg['from']['username']
            else:
                user = msg['from']['first_name'] 

            bot.sendMessage(chat_id, user + ' rolled' + action_text + ':\r\n'
                + ', '.join(dice) + ' = ' + str(value) + ' =\r\n' +  
                sign + str(result) + ' ' + ladder_result
            )

TOKEN = sys.argv[1] # get token from command line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening...')

# Keep the program running
while 1:
    time.sleep(10)
