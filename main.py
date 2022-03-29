import os

from telegram import Bot
from telegram.ext import Updater, CommandHandler
from commands import *

# from keep_alive import keep_alive

TOKEN = os.getenv("TOKEN")

if (not TOKEN):
    raise Exception("No Telegram token in Enviroiment found!")

bot = Bot(token=TOKEN)


def main():
    updater = Updater(TOKEN)

    commands = {
        'help': help_command,
        'signup': new_signup,
        'signout': new_signout,
        'newgame': new_new_game,
        'startgame': new_start_game,
    }

    dispatcher = updater.dispatcher

    for command, method in commands.items():
        dispatcher.add_handler(CommandHandler(command, method))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
