import os

from telegram import Update, Bot, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext

from game import distribute_roles
# from replit import db
from keep_alive import keep_alive

bot = Bot(token=os.getenv("TOKEN"))

# Statt in die DB zu schreiben, schreiben wir aktuelle Daten
# hier rein
games = {}


def getGroupChatId(update) -> str:
    return str(update.message['chat']['id'])


def help_command(update: Update, context: CallbackContext) -> None:
    htext = '''
Wilkommen
Commands: 
    /help
    /newgame Traitor:1 Jester:1Z
    /signup
    /startgame
'''
    bot.sendMessage(chat_id=int(update.message['chat']['id']), text=htext, parse_mode=ParseMode.MARKDOWN)



def signout(update: Update, context: CallbackContext) -> None:
    '''
        Wenn man grad einer lobby gejoint ist, um diese wieder zu verlassen
    '''
    groupChatId = getGroupChatId(update)
    # Funktioniert nur in Gruppenchat
    if update.message['chat']['type'] == "group":

        # Wenn für die Gruppe noch kein Dict im Games Dict angelegt wurde
        if groupChatId not in games.keys():
            games[groupChatId] = {'players': []}

        # User Objekt aus Vorname und UserId
        user = {
            'name': update.message.from_user.first_name,
            'chat': update.message.from_user['id'],
        }

        # Nur wenn der User überhaupt gejoint ist, kann er verlassen
        if user in games[groupChatId]['players']:
            index = games[groupChatId]['players'].index(user)
            games[groupChatId]['players'].pop(index)

            # Nachricht mit aktuellem Spiel editieren und Spieler hinzufügen
            currGameMsgId = games[groupChatId]['currentGameMsgId']

            players = games[groupChatId]['players']

            bot.edit_message_text(chat_id=int(groupChatId),
                                  text=("*Spieler*: \n" +
                                        "\n".join([p['name']
                                                   for p in players])),
                                  message_id=currGameMsgId,
                                  parse_mode=ParseMode.MARKDOWN)


def signup(update: Update, context: CallbackContext) -> None:
    groupChatId = getGroupChatId(update)
    if update.message['chat']['type'] == "group":
        if groupChatId not in games.keys():
            games[groupChatId] = {'players': []}
        user = {
            'name': update.message.from_user.first_name,
            'chat': update.message.from_user['id'],
        }
        if user not in games[groupChatId]['players']:
            games[groupChatId]['players'].append(user)

            # Nachricht mit aktuellem Spiel editieren und Spieler hinzufügen
            if 'currentGameMsgId' in games[groupChatId].keys():
                currGameMsgId = games[groupChatId]['currentGameMsgId']

                players = games[groupChatId]['players']

                bot.edit_message_text(chat_id=int(groupChatId),
                                      text=getPlayerListGameText(players),
                                      message_id=currGameMsgId,
                                      parse_mode=ParseMode.MARKDOWN)


def getPlayerListGameText(players):
    return ("*Spieler*: \n" + "\n".join([p['name'] for p in players]))


def parseNewGameArgs(args):
    params = args.replace(',', '.').split(' ')[1:]
    params = [p.split(':') for p in params]
    roles = {}
    for role, factor in params:
        roles[role.strip()] = factor

    if roles == {}:
        raise "Keine Rollen vergeben"

    return roles


def new_game(update: Update, context: CallbackContext) -> None:
    groupChatId = getGroupChatId(update)
    games[groupChatId] = {'players': []}

    try:
        args = update.message['text']

        games[groupChatId]['roles'] = parseNewGameArgs(args)

        players = games[groupChatId]['players']
        user = {
            'name': update.message.from_user.first_name,
            'chat': update.message.from_user['id'],
        }

        if user not in games[groupChatId]['players']:
            games[groupChatId]['players'].append(user)

        newGameMsgId = bot.sendMessage(text=getPlayerListGameText(players),
                                       chat_id=int(groupChatId),
                                       parse_mode=ParseMode.MARKDOWN)

        # die Nachricht des aktuellen Spiels in das GruppenChat Dict schreiben
        games[groupChatId]['currentGameMsgId'] = newGameMsgId.message_id

    except:
        bot.sendMessage(text="Falsches Format!",
                        chat_id=int(groupChatId),
                        parse_mode=ParseMode.MARKDOWN)


def start_game(update: Update, context: CallbackContext) -> None:
    '''
    '''
    groupChatId = getGroupChatId(update)
    try:
        all_player = games[groupChatId]['players']

        if (len(all_player) < 2):
            bot.sendMessage(int(groupChatId),
                            "Nicht genügend Spieler (min. 2)")
            return

        # Spieler den Rollen aufteilen
        roles = games[groupChatId]['roles']
        player_roles = distribute_roles(all_player, roles)

        all_user_reachable = True
        for role, players in player_roles.items():
            for player in players:
                try:
                    # Jedem Spieler seine Rolle mitteilen
                    bot.sendMessage(player['chat'], f"Du bist {role}")

                    # Wenn mehrere Traiter -> andere Traitor mitteilen
                    # Außerdem erfahren sie, wer alles Jester ist
                    if role == "Traitor":
                        extra_msg = ""

                        # Traitor Kollegen: \n Player1 \n Player2 ...
                        extra_msg += ("Traitor Kollegen:\n" + "\n".join(
                            [p['name'] for p in players if p != player]) +
                                      "\n\n") if len(players) > 1 else ""

                        # Jester: \n Player1 \n Player2 ...
                        extra_msg += (f"Jester:\n" + "\n".join(
                            [p['name'] for p in player_roles["Jester"]])
                                      ) if "Jester" in player_roles else ""

                        if extra_msg.strip() != "":
                            bot.sendMessage(player['chat'], extra_msg.strip())

                except Exception as e:
                    print(e)
                    all_user_reachable = False
                    bot.sendMessage(
                        int(groupChatId),
                        f"*Fehler Aufgetreten:*\n{player['name']} muss erst dem Bot privat schreiben! ",
                        ParseMode.MARKDOWN)
        if all_user_reachable:
            participant = "*Teilnehmer:*\n" + "\n".join(
                [player['name'] for player in all_player])
            # distribution = "\n\n" + "\n".join([f"{rolename}: {len(role)}" for rolename, role in player_roles.items()])
            bot.sendMessage(int(groupChatId), participant, ParseMode.MARKDOWN)

    except:
        bot.sendMessage(
            int(groupChatId),
            "Bitte zuerst ein Spiel starten mit /newgame Traitor:2 Jester:1Z ..."
        )


def main():
    updater = Updater(os.getenv("TOKEN"))

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
    keep_alive()
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            admins = json.loads(os.environ['ADMINS'])
            for admin in admins:
                bot.sendMessage(int(admin), str(e))
"""
Define command palette for Telegram Client
1. Nachricht an @BotFather mit /setcommands
2. Bot auswählen
3. senden: 

newgame - Erstelle neue leere Lobby
startgame - Startet das aktuelle Spiel
signup - Am aktuellen Spiel teilnehmen
signout - Aus aktuellem Spiel abmelden

###
"""
