#!/bin/python
import sys
import time
import telepot
import random
import re

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

class Input:
    def __init__(self):
        self.isset = False
        self.is_command = False
        self.commands = [
            '/r',
            '/roll',
            '/rf'
        ]

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

    def get_params(self):
        # Set defaults
        parameters = {}
        parameters['modifier'] = ''
        parameters['label'] = ''
        
        # Get parameters if provided
        if len(self.content_list) >= 2:
            try: 
                if isinstance(eval(self.content_list[1]), int):
                    parameters['modifier'] = self.content_list[1]
                    labelat = 2
            except NameError:
                labelat = 1

            if len(self.content_list) >= (labelat + 1):
                msg_begin, keyword, msg_end = self.content.partition(self.content_list[labelat])
                parameters['label'] = ' ' + keyword + msg_end
        return parameters

    # Roll dice
    def roll(self):
        if self.content_list[0] == '/rf':
            parameters = self.get_params()
            if len(parameters['modifier']):
                self.equation = '4dF+' + str(parameters['modifier'])
            else:
                self.equation = '4dF'
        else: 
            self.equation = self.content_list[1]

        equation_list = re.split('+ |- |* |/', self.equation)
        print(equation_list)

        result = []

        counter = 0
        value = 0

        individual_dice = []
        dice = []

        while counter < 4:
            choice = random.choice(list(options.keys()))
            individual_dice.append(options[choice])
            value += choice
            counter += 1

        dice.append(individual_dice)
        dice.append(value)
        result.append(dice)
        return result

    def process(self):
        #Get list of dice in content
        #if self.content_list[1] == '' #Regex representing dice notation equation
        #
        #rolls = []

        outcome = self.roll()
        result = eval(str(outcome[0][1]))

        # Set die results plus modifier
        if len(self.parameters['modifier']):
            final_result = str(result) + ' + ' + str(self.parameters['modifier'])
        else:
            final_result = str(result)

        # Set if final result is positive or negative
        if eval(final_result) > -1:
            sign = '+'
        else:
            sign = ''

        # Set ladder value for final result
        if eval(final_result) < -2:
            ladder_result = 'Beyond Terrible'
        elif eval(final_result) > 8:
            ladder_result = 'Beyond Legendary'
        else:
            ladder_result = ladder[eval(final_result)]

        response = (self.user + ' rolled' + self.parameters['label'] + ':\r\n'        
            + ' '.join(outcome[0][0]) + ' = ' + final_result + ' =\r\n' +  
            sign + str(eval(final_result)) + ' ' + ladder_result)

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
