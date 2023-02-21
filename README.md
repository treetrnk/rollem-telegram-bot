# RollEm Telegram Bot
Um bot de rolagem de dados poliédricos para [Telegram](https://telegram.org). Para usar este bot no Telegram, [clique aqui](https://t.me/sddicerollbot). Este bot foi construído para permitir a jogabilidade de jogos de mesa de RPG (RPGs) no Telegram.

## Requerimentos
* python-telegram-bot - Veja https://github.com/python-telegram-bot/python-telegram-bot para instruções de instalação.

## Recursos Atuais

* `/roll [equação] [rótulo]` ou `/r [equação] [rótulo]`  
    * A equação é obrigatória, o rótulo é opcional. 
    * Role dados usando [notação de dados](https://en.wikipedia.org/wiki/Dice_notation) como equação (inclui dados Fate/Fudge com 4dF). Não inclua espaços na equação. 
    * Exemplo: `/roll 4d8+16-2d4`
    * Dados explosivos com ponto de exclamação: `/r 6d6!` (Caso o dado seja o maior número possível, ele será rolado novamente e somado ao resultado anterior)
    * Dados mais altos e mais baixos mantidos para vantagem/desvantagem: `/r 2d20H Advantage`
* `/rf [modificador] [rótulo]`
    * O modificador e o rótulo são opcionais, mas se ambos forem fornecidos, o modificador deve vir primeiro.
    * Role 4 dados Fate (Fudge).
    * Exemplo: `/rf 3 Atletismo`

**[VEJA A WIKI](https://github.com/miguelvieirart/rollem-telegram-bot/wiki) para instruções de uso e exemplos.**

## Solução de Problemas

Se você estiver recebendo um erro que diz `Server response could not be decoded using UTF-8`, faça as seguintes alterações no arquivo requests.py do python-telegram-bot: [Bug Fix Diff](https://github.com/python-telegram-bot/python-telegram-bot/pull/1623/files)