import os

from telegram import Bot
from telegram.ext import Updater, CommandHandler
from commands import *

# from keep_alive import keep_alive

TOKEN = os.getenv("TOKEN")

if (not TOKEN):
    raise Exception("No Telegram Token in Enviroiment found!")

bot = Bot(token=TOKEN)


def main():
    updater = Updater(TOKEN)

    commands = {
        'start': help_command,
        'help': help_command,
        'signup': signup,
        'signin': signup,
        'signout': signout,
        'newgame': new_game,
        'startgame': start_game,
    }

    dispatcher = updater.dispatcher

    for command, method in commands.items():
        dispatcher.add_handler(CommandHandler(command, method))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    import json
    # keep_alive()
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            admins = json.loads(os.environ['ADMINS'])
            for admin in admins:
                bot.sendMessage(int(admin), str(e))
