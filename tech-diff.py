#! /home/nathan/.virtualenvs/rollem/bin/python
import sys
import time
import re
import random
import traceback
import unicodedata
import logging
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler
from codecs import encode,decode
from datetime import datetime
from ast import literal_eval

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

fate_options = { 
        -1 : '[-]', 
        0  : '[  ]', 
        1  : '[+]' 
    }

def rf(bot, update, args):
    if len(args) > 0:
        args[0] = '4df+' + str(args[0])
    else:
        args = ['4df']
    roll(bot, update, args)


def roll(bot, update, args):
    equation = args[0].strip() if len(args) > 0 else False
    equation_list = re.findall(r'(\w+!?>?\d*)([+*/()-]?)', equation)
    print(equation_list)
    comment = args[1] if len(args) > 1 else False
    space = ''
    is_fate = False
    use_ladder = False
    result = {
        'visual': [],
        'equation': [],
        'total': ''
    }

    for pair in equation_list:
        for item in pair:
            dice = re.search(r'(\d*)d([0-9fF]+)(!>[0-9]+|!)?', item)
            if item and dice.group(1) and dice.group(2):
                dice_num = dice.group(1) if dice.group(1) else 1
                sides = dice.group(2)
                if sides > 1000:
                    raise Exception('Maximum number of rollable dice is 100')
                space = ' '
                result['visual'].append(space + '(')
                result['equation'].append('(')
                fate_dice = ''
                current_die_results = ''
                plus = ''

                while sides > 0:
                    if sides in ['f','F']:
                        is_fate = True
                        use_ladder = True
                        current_fate_die = random.choice(list(self.fate_options.keys()))
                        current_die_results += plus + str(current_fate_die)
                        fate_dice += fate_options[current_fate_die] + ' '
                    else:
                        sides = int(sides)
                        last_roll = random.randint(1,int(dice.group(2)))
                        current_die_results += plus + str(last_roll)
                        sides -= 1
                    if len(plus) is 0: # Adds all results to result unless it is the first one
                        plus = ' + '
                    if is_fate:
                        is_fate = False
                        result['visual'].append(' ' + fate_dice)
                    else:
                        result['visual'].append(current_die_results)
                    result['equation'].append(current_die_results)
                    result['visual'].append(')')
                    result['equation'].append(')')
            else:
                if item


    '''
    #try:
    for pair in equation_list:
        print(f'pair: {pair}')
        for i in pair:
            print(f'i: {i}')
            min_explosion = -1
            explodes = False
            dice = re.search(r'(\d*)d([0-9fF]+)(!>[0-9]+|!)?', (i))
            print(dice)
            #Check if explosion is valid
            if dice:
                # Set number of dice to roll
                if len(dice.group(1)):
                    loop_num = int(dice.group(1)) 
                else:
                    loop_num = 1

                if loop_num > 1000:
                    raise Exception('Maximum number of rollable dice is 100')
                if dice.group(3) and int(dice.group(2)) >= 2:
                    explodes = True
                    die_sides = int(dice.group(2))
                    if len(dice.group(3)) > 1:
                        num = int(dice.group(3)[2:]) + 1
                        if num > die_sides:
                            raise Exception(
                                'Explosion minimum value must be lower or equal to the die\'s sides number!')
                        else:
                            min_explosion = num
                    else:
                        min_explosion = die_sides
                result['visual'].append(space + '(')
                result['equation'].append('(')
                space = ' '
                fate_dice = ''
                current_die_results = ''
                plus = ''
                
                # Roll dice
                while loop_num > 0:
                    if dice.group(2) == 'f' or dice.group(2) == 'F':
                        is_fate = True
                        current_fate_die = random.choice(list(self.fate_options.keys()))
                        current_die_results += plus + str(current_fate_die)
                        fate_dice += fate_options[current_fate_die] + ' '
                    else:
                        last_roll = random.randint(1,int(dice.group(2)))
                        current_die_results += plus + str(last_roll)
                        if explodes and (last_roll >= min_explosion):
                            loop_num += 1
                    if len(plus) is 0: # Adds all results to result unless it is the first one
                        plus = ' + '
                    loop_num -= 1
                    if is_fate:
                        is_fate = False
                        use_ladder = True
                        result['visual'].append(' ' + fate_dice)
                    else:
                        result['visual'].append(current_die_results)
                    result['equation'].append(current_die_results)
                    result['visual'].append(')')
                    result['equation'].append(')')
                else:
                    result['visual'].append(' ')
                    result['visual'].append(i)
                    result['equation'].append(i)

        result['total'] = str(''.join(result['equation'])).replace(" ","").replace('(','').replace(')','')
        if bool(re.match('^[0-9+*/ ()-]+$', result['total'])):
            result['total'] = eval(result['total'])
        else:
            raise Exception('Request was not a valid equation!')

        print(''.join(result['equation']) + ' = ' + str(result['total']))

        if use_ladder:
            get_ladder()

        # Only show part of visual equation if bigger than 300 characters
        result['visual'] = ''.join(result['visual'])
        if len(self.result['visual']) > 275:
            result['visual'] = result['visual'][0:275] + ' . . . )'

        response = (' rolled<b>' + self.label + '</b>:\r\n'        
            + self.result['visual'] + ' =\r\n<b>' + str(self.result['total']) + '</b>')
        error = ''

    '''
    #except Exception as e:
    #    response = (': <b>Invalid equation!</b>\r\n' +
    #        'Please use <a href="https://en.wikipedia.org/wiki/Dice_notation">dice notation</a>.\r\n' +
    #        'For example: <code>3d6</code>, or <code>1d20+5</code>, or <code>d12</code>\r\n\r\n' +
    #        'For more information, type <code>/help</code>'
    #        )
    #    print(e)
    #    print(response)
    #    error = traceback.format_exc().replace('\r', '').replace('\n', '; ')

        #logfile.write('\r\n\r\n' + str(datetime.now()) + '======================================\r\n')
        #logfile.write('\tRESPONSE: ' + response.replace('\r', ' ').replace('\n', '') + '\r\n')
        #if len(error):
        #    logfile.write('\tERROR: ' + error + '\r\n')

    bot.send_message(chat_id=update.message.chat_id, text=response, parse_mode=ParseMode.HTML)


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

roll_handler = CommandHandler(['roll','r'], roll, pass_args=True)
dispatcher.add_handler(roll_handler)

roll_handler = CommandHandler('rf', rf, pass_args=True)
dispatcher.add_handler(roll_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
         level=logging.INFO)

updater.start_polling()
