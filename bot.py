import sys
import re
import random
import traceback
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


# CONFIGURATION

TOKEN = sys.argv[1]

NATTWENTY = False
HLTEXT = False

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ladder = {
    8  : 'Lendário',	
    7  : 'Épico',
    6  : 'Fantástico',
    5  : 'Excelente',
    4  : 'Ótimo',
    3  : 'Bom',
    2  : 'Razoável',
    1  : 'Médio',
    0  : 'Mediocre',
    -1 : 'Ruim',
    -2 : 'Terrível'

}

fate_options = { 
    -1 : '[-]', 
    0  : '[  ]', 
    1  : '[+]' 
}

# HELPERS

def get_ladder(result):
    if result > 8:
        return 'Mais que lendário'
    elif result < -2:
        return 'Terrível'
    else:
        return ladder[result]

# FUNCTIONS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Digite /help para obter ajuda.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
    message_thread_id = update.message.message_thread_id if update.message.message_thread_id else None
    help_file = open('help.html', 'r', encoding='utf-8')
    response = (help_file.read())
    help_file.close()
    logging.info(f'@{username} | /help')
    # job = context.job
    # Convert to utf-8
    await context.bot.send_message(chat_id=update.message.chat_id, text=response, parse_mode='html', disable_web_page_preview=True, message_thread_id=message_thread_id)
    

async def rf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.debug(context.args)
    if len(context.args) > 0:
        context.args[0] = '4df+' + str(context.args[0])
    else:
        context.args = ['4df']
    process(update, context)

async def process(update: Update, context: ContextTypes.DEFAULT_TYPE):

    is_forwarded = False

    if update.message.forward_from or update.message.forward_from_chat or update.message.forward_from_message_id or update.message.forward_signature or update.message.forward_sender_name or update.message.forward_date:
        is_forwarded = True

    if is_forwarded:
        return

    username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name

    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Digite /help para obter ajuda.")
        return

    # Get the message_thread_id from the message if it exists and prevent errors if it doesn't
    message_thread_id = update.message.message_thread_id if update.message.message_thread_id else None

    equation = context.args[0].strip()
    equation_list = re.findall(r'(\w+!?>?\d*)([+*/()-]?)', equation)
    comment = ' ' + ' '.join(context.args[1:]) if len(context.args) > 1 else ''
    space = ''
    dice_num = None
    original_dice_num = None
    is_fate = False
    use_ladder = False
    nat20text = ''
    high_low_helper = ''
    if '2d20' in equation.lower() and not ('2d20h' in equation.lower() or '2d20l' in equation.lower()) and HLTEXT:
        # high_low_helper = 'Get the highest or lowest dice from a roll with H and L.\r\nType <code>/help</code> for more info.\r\n\r\n'
        high_low_helper = 'Obtenha o dado mais alto ou mais baixo de uma rolagem com H e L.\r\nDigite <code>/help</code> para mais informações.\r\n\r\n'
    result = {
        'visual': [],
        'equation': [],
        'total': ''
    }

    try:
        for pair in equation_list:
            logging.debug(f"pair: {pair}")
            pair = [i for i in pair if i]
            for item in pair:
                logging.debug(f"item: {item}")
                if item and len(item) > 1 and any(d in item for d in ['d', 'D']):
                    dice = re.search(r'(\d*)d([0-9f]+)([!hl])?', item.lower())
                    dice_num = int(dice.group(1)) if dice.group(1) else 1
                    original_dice_num = dice_num
                    if dice_num > 1000:
                        # raise Exception('Maximum number of rollable dice is 1000')
                        raise Exception('O número máximo de dados roláveis é 1000')
                    sides = dice.group(2)
                    space = ' '
                    result['visual'].append(space + '(')
                    result['equation'].append('(')
                    fate_dice = ''
                    current_die_results = ''
                    current_visual_results = ''
                    plus = ''
                    explode = False
                    highest = False
                    lowest = False
                    if dice.group(3) and dice.group(3)[0] == '!' and int(dice.group(2)) > 1:
                        explode = True 
                    elif dice.group(3) and dice.group(3)[0] in ['h','H']:
                        highest = True
                    elif dice.group(3) and dice.group(3)[0] in ['l','L']:
                        lowest = True

                    random_start_num = 1
                    if sides in ['f','F']:
                        is_fate = True
                        use_ladder = True
                        sides = 1
                        random_start_num = -1
                    else:
                        sides = int(sides)

                    while dice_num > 0:
                        
                        last_roll = random.randint(random_start_num, sides)
                        visual_last_roll = plus + str(last_roll)
                        if is_fate:
                            visual_last_roll = fate_options[last_roll] + ' '
                        current_visual_results +=  visual_last_roll

                        if (highest or lowest) and current_die_results:
                            #print(current_die_results)
                            if highest:
                                if last_roll > int(current_die_results):
                                    current_die_results = str(last_roll)
                            else: #lowest
                                if last_roll < int(current_die_results):
                                    current_die_results = str(last_roll)
                        else:
                            current_die_results += plus + str(last_roll)

                        if not (explode and last_roll == sides):
                            dice_num -= 1

                        if len(plus) == 0: 
                            # Adds all results to result unless it is the first one
                            plus = ' + '

                        if sides == 20 and last_roll == 20 and original_dice_num < 3 and '20' in current_die_results and NATTWENTY:
                            # nat20text = '    #Natural20'
                            nat20text = '    #20Natural'

                    if is_fate:
                        is_fate = False
                    result['visual'].append(current_visual_results)
                    result['equation'].append(current_die_results)
                    result['visual'].append(')')
                    result['equation'].append(')')
                    if highest or lowest:
                        result['visual'].append(dice.group(3)[0])
                else:
                    if item and (item in ['+','-','/','*',')','('] or int(item)):
                        result['visual'].append(' ')
                        result['visual'].append(item)
                        result['equation'].append(item)

        result['total'] = str(''.join(result['equation'])).replace(" ","")
        if bool(re.match('^[0-9+*/ ()-]+$', result['total'])):
            result['total'] = eval(result['total'])
        else:
            # raise Exception('Request was not a valid equation!')
            raise Exception('A solicitação não era uma equação válida!')

        if use_ladder:
            # Set if final result is positive or negative
            sign = '+' if result['total'] > -1 else ''
            ladder_result = get_ladder(result['total'])
            result['total'] = sign + str(result['total']) + ' ' + ladder_result

        # Only show part of visual equation if bigger than 300 characters
        result['visual'] = ''.join(result['visual'])
        if len(result['visual']) > 275:
            result['visual'] = result['visual'][0:275] + ' . . . )'

        logging.info(f'@{username} | ' + ' '.join(context.args) + ' = ' + ''.join(result['equation']) + ' = ' + str(result['total']) + nat20text)
        # response = (f'{high_low_helper}@{username} rolled<b>{comment}</b>:\r\n {result["visual"]} =\r\n<b>{str(result["total"])}</b>{nat20text}')
        response = (f'{high_low_helper}@{username} rolou<b>{comment}</b>:\r\n {result["visual"]} =\r\n<b>{str(result["total"])}</b>{nat20text}')
        error = ''

    except Exception as e:
        # response = f'@{username}: <b>Invalid equation!</b>\r\n'
        response = f'@{username}: <b>Equação inválida!</b>\r\n'
        if dice_num and dice_num > 1000:
            response += str(e) + '.\r\n'
        # response += ('Please use <a href="https://en.wikipedia.org/wiki/Dice_notation">dice notation</a>.\r\n' +
        #         'For example: <code>3d6</code>, or <code>1d20+5</code>, or <code>d12</code>\r\n\r\n' +
        #         'For more information, type <code>/help</code>'
        #     )
        response += ('Por favor, use <a href="https://en.wikipedia.org/wiki/Dice_notation">notação de dados</a>.\r\n' +
                'Por exemplo: <code>3d6</code>, ou <code>1d20+5</code>, ou <code>d12</code>\r\n\r\n' +
                'Para mais informações, digite <code>/help</code>'
            )
        error = traceback.format_exc().replace('\r', '').replace('\n', '; ')
        # logging.warning(f'@{username} | /r {equation} | RESPONSE: Invalid Equation |\r\n{error}')
        logging.warning(f'@{username} | /r {equation} | RESPONSE: Equação inválida |\r\n{error}')

    await context.bot.send_message(chat_id=update.message.chat_id, text=response, parse_mode='html', message_thread_id=message_thread_id)

# MAIN
    
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    roll_handler = CommandHandler(['r','roll'], process)
    application.add_handler(roll_handler)

    roll_handler = CommandHandler('rf', rf)
    application.add_handler(roll_handler)
    
    application.run_polling()