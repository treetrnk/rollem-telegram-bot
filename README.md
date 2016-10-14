# RollEm Telegram Bot
A polyhedral dice rolling bot for [Telegram](https://telegram.org). To use this bot in Telegram, [click here](https://telegram.me/rollembot). This bot was built to enable playing tabletop roleplaying games (RPGs) over Telegram.

## Requires
* Telepot - See https://github.com/nickoala/telepot for installation instructions.

## Current Features
* `/roll [equation] [label]` or `/r [equation] [label]`  
 * Equation is required, label is optional. 
 * Roll dice using [dice notation](https://en.wikipedia.org/wiki/Dice_notation) as the equation (includes Fate/Fudge Dice with 4dF). Do not include spaces in the equation. 
 * Example: `/roll 4d8+16-2d4`
* `/rf [modifier] [label]`  
 * The modifier and label are optional, but if both are given the modifier must come first.
 * Roll 4 Fate (Fudge) dice.
 * Example: `/rf 3 Athletics` 

## Planned Features
* Dice macros
* NPC name generator (maybe?)
* Aspect generator (maybe?)
