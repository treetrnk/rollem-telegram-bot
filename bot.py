#!/bin/python
import sys
import time
import telepot
import random

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
            if self.content.startswith('/roll') or self.content.startswith('/r'):
                self.is_command = True

        print(self.content_type, self.chat_type, self.chat_id)

    # Roll dice
    def roll(self, notation):
        result = []
        for die_roll in notation:
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


    def respond(self):
        #Get list of dice in content
        #if self.content_list[1] == '' #Regex representing dice notation equation
        #
        #rolls = []

        outcome = self.roll(['4dF'])
        parameters = self.get_params()
        result = eval(str(outcome[0][1]))

        # Set die results plus modifier
        if len(parameters['modifier']):
            final_result = str(result) + ' + ' + str(parameters['modifier'])
        else:
            final_result = str(result)

        # Set if final result is positive or negative
        if eval(str(final_result)) > -1:
            sign = '+'
        else:
            sign = ''

        # Set ladder value for final result
        if eval(str(final_result)) < -2:
            ladder_result = 'Beyond Terrible'
        elif eval(str(final_result)) > 8:
            ladder_result = 'Beyond Legendary'
        else:
            ladder_result = ladder[result]

        # === Uncomment for Debugging ===
        # print(msg)

        # Respond to user with results
        bot.sendMessage(self.chat_id, self.user + ' rolled' + parameters['label'] + ':\r\n'
            + ' '.join(outcome[0][0]) + ' = ' + final_result + ' =\r\n' +  
            sign + str(eval(final_result)) + ' ' + ladder_result
        )

current_input = Input()

def handle(msg):
    current_input.set_attrbs(msg)
    if current_input.is_command:
        current_input.respond()

TOKEN = sys.argv[1] # get token from command line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening...')

# Keep the program running
while 1:
    time.sleep(10)
