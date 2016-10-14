#!/bin/python
import sys
import time
import telepot
import random
import re

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

class Input:
    def __init__(self):
        self.isset = False
        self.is_command = False
        self.commands = [
            '/r',
            '/roll',
            '/rf'
        ]

    ####################
    ## Set Attributes ##
    ####################
    def set_attrbs(self, msg):
        self.isset = True
        self.msg = msg
        self.content_type, self.chat_type, self.chat_id = telepot.glance(msg)
        if 'username' in msg['from'].keys():
            self.user = msg['from']['username']
        else:
            self.user = msg['from']['first_name'] 

        #Get command
        self.is_command = False
        if self.content_type == 'text':
            self.content = msg['text']
            self.content_list = self.content.split()
            if self.content_list[0] in self.commands:
                self.is_command = True

        print(self.content_type, self.chat_type, self.chat_id)

    ####################
    ## Get Parameters ## Can be dissolved into Roll() I think
    ####################
    def get_params(self):
        # Set defaults
        self.parameters = {}
        self.parameters['modifier'] = ''
        self.parameters['label'] = ''
        labelat = 2
        
        if self.content_list[0] == '/rf':
            # Get parameters if provided
            if len(self.content_list) >= 2:
                try: 
                    if isinstance(eval(self.content_list[1]), int):
                        self.parameters['modifier'] = self.content_list[1]
                        labelat = 2
                except NameError:
                    labelat = 1

            if len(self.content_list) >= (labelat + 1):
                msg_begin, keyword, msg_end = self.content.partition(self.content_list[labelat])
                self.parameters['label'] = ' ' + keyword + msg_end
        elif len(self.content_list) >= 3:
            self.parameters['label'] = ' ' + ' '.join(content_list(range(2,len(content_list))))
        return 

    ################
    ##  Roll dice ##
    ################
    def roll(self):
        self.get_params()
        # Set equation to 4dF if /rf shortcut was usedd
        if self.content_list[0] == '/rf':
            if len(self.parameters['modifier']):
                self.equation = '4dF+' + str(self.parameters['modifier'])
            else:
                self.equation = '4dF'
        else: 
            self.equation = self.content_list[1]

        fate_options = { 
            -1 : '[‒]', 
            0  : '[  ]', 
            1  : '[+]' 
        }

        result = []
        self.fate_dice = []

        print(self.equation)
        # Break apart equation by operators
        equation_list = re.findall(r'(\w+)([+*/-]?)', self.equation)
        print(equation_list)
        # Break apart each chunk of the equation by numbers and letters 
        # if dice notation
        for pair in equation_list:
            for i in pair:
                dice = re.search(r'(\d*)d([0-9fF]+)', str(i))
                if dice:
                    # Set number of dice to roll
                    if len(dice.group(1)):
                        loop_num = eval(str(dice.group(1))) 
                    else:
                        loop_num = 1
                    
                    current_die_results = ''
                    plus = ''
                    # Roll dice
                    while loop_num > 0:
                        if dice.group(2) == 'f' or dice.group(2) == 'F':
                            current_fate_die = random.choice(list(fate_options.keys()))
                            current_die_results += plus + str(current_fate_die)
                            self.fate_dice.append(fate_options[current_fate_die])
                        else: 
                            current_die_results += plus + str(random.randint(1,eval(dice.group(2))))
                        if len(plus) is 0: # Adds all results to result unless it is the first one
                            plus = ' + '
                        loop_num -= 1
                    
                    result.append(current_die_results)
                else:
                    result.append(i)

        print(result)

        if len(self.fate_dice):
            self.fate_dice.append('\r\n')

        return result

    #####################
    ## Process Message ##
    #####################
    def process(self):

        dice_results = self.roll()
        total = eval(str(''.join(dice_results)))

        if len(self.fate_dice):
            # Set if final result is positive or negative
            if total > -1:
                sign = '+'
            else:
                sign = ''

            # Set ladder value for final result
            if total < -2:
                ladder_result = 'Beyond Terrible'
            elif total > 8:
                ladder_result = 'Beyond Legendary'
            else:
                ladder_result = ladder[total]

            total = sign + str(total) + ' ' + ladder_result

        response = (self.user + ' rolled' + self.parameters['label'] + ':\r\n'        
            + ' '.join(self.fate_dice) + ''.join(dice_results) + 
            ' =\r\n' + str(total))

        # Respond to user with results
        bot.sendMessage(self.chat_id, response)

        # === Uncomment for Debugging ===
        # print(msg)
    
current_input = Input()

def handle(msg):
    current_input.set_attrbs(msg)
    if current_input.is_command:
        current_input.process()

TOKEN = sys.argv[1] # get token from command line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening...')

# Keep the program running
while 1:
    time.sleep(10)
