# RollEm Telegram Bot
A polyhedral dice rolling bot for [Telegram](https://telegram.org). To use this bot in Telegram, [click here](https://telegram.me/rollembot). This bot was built to enable playing tabletop roleplaying games (RPGs) over Telegram.

## Requires
* python-telegram-bot - See https://github.com/python-telegram-bot/python-telegram-bot for installation instructions.

## Current Features
* `/roll [equation] [label]` or `/r [equation] [label]`  
    * Equation is required, label is optional. 
    * Roll dice using [dice notation](https://en.wikipedia.org/wiki/Dice_notation) as the equation (includes Fate/Fudge Dice with 4dF). Do not include spaces in the equation. 
    * Example: `/roll 4d8+16-2d4`
    * Exploding dice with exclamation point: `/r 6d6!`
    * Highest and Lowest dice kept for advantage/disadvantage: `/r 2d20H Advantage`
* `/rf [modifier] [label]`  
    * The modifier and label are optional, but if both are given the modifier must come first.
    * Roll 4 Fate (Fudge) dice.
    * Example: `/rf 3 Athletics` 

**[SEE THE WIKI](https://github.com/treetrnk/rollem-telegram-bot/wiki) for usage instructions and examples.**

## Troubleshooting

If you are receiving an error that says `Server response could not be decoded using UTF-8`, make the following changes to the python-telegram-bot requests.py file: [Bug Fix Diff](https://github.com/python-telegram-bot/python-telegram-bot/pull/1623/files)
