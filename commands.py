from helpers import *
from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from typing import TypedDict


# {'412823595':
#   {
#     'players': []},
#     '-660992491': {
#            'players': [
#              {'name': 'Sebastian', 'chat': 412823595}
#              ],
#              'roles': {'Traitor': '1'},
#              'currentGameMsgId': 2927
#       }
#    }


class Player(TypedDict):
    name: str
    chat: int


class Game(TypedDict):
    players: list[Player]
    roles: dict[str, str]
    currentGameMsgId: int


# Beinhaltet die aktuellen Spiele
games: dict[str, Game] = {}


def help_command(update: Update, context: CallbackContext) -> None:
    bot = context.bot

    htext = '''
Wilkommen
Commands: 
    /help
    /newgame Traitor:1 Jester:1Z
    /signup
    /startgame
'''
    bot.sendMessage(chat_id=int(
        update.message['chat']['id']), text=htext, parse_mode=ParseMode.MARKDOWN)


def signout(update: Update, context: CallbackContext) -> None:
    '''
    Wenn man grad einer Lobby gejoint ist, um diese wieder zu verlassen
    '''
    bot = context.bot

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
    bot = context.bot
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
    print(games)


def new_game(update: Update, context: CallbackContext) -> None:
    bot = context.bot
    groupChatId = getGroupChatId(update)
    games[groupChatId] = {'players': []}

    try:
        args = update.message['text']
        print(update.message.text)

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
    Startet das Spiel mit den bisher gejointen Spielern und sendet diesen
    eine DM mit deren zufällig zugeteilten Rolle
    '''
    bot = context.bot
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
            bot.sendMessage(int(groupChatId), participant, ParseMode.MARKDOWN)

    except:
        bot.sendMessage(
            int(groupChatId),
            "Bitte zuerst ein Spiel starten mit /newgame Traitor:2 Jester:1Z ..."
        )
