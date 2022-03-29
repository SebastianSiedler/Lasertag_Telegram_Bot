import os

from telegram.ext import Updater, CommandHandler
from commands import *

TOKEN = os.getenv("TOKEN")

if (not TOKEN):
    raise Exception("No Telegram token in Enviroiment found!")


def main():
    updater = Updater(TOKEN)

    commands = {
        'help': help_command,
        'signup': new_signup,
        'signout': new_signout,
        'newgame': new_new_game,
        'startgame': new_start_game,
    }

    for command, method in commands.items():
        updater.dispatcher.add_handler(CommandHandler(command, method))

    print("Bot is running...", flush=True)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
