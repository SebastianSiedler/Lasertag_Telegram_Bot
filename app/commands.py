from telegram import ParseMode, Update
from game import GameDB
from telegram.ext import CallbackContext

games_db = GameDB()


def new_signup(update: Update, context: CallbackContext) -> None:
    bot = context.bot
    group_chat_id = update.message.chat.id

    try:
        game = games_db.find_game(group_chat_id)

        if (game == None):
            raise Exception("No game found")

        game.add_player(
            name=update.message.from_user.first_name,
            id=update.message.from_user.id
        )

        bot.edit_message_text(
            chat_id=group_chat_id,
            text=game.get_player_list_game_text(),
            message_id=game.current_game_msg_id,
            parse_mode=ParseMode.MARKDOWN
        )

    except Exception as e:
        bot.send_message(
            text=str(e),
            chat_id=group_chat_id
        )
        raise e


def new_signout(update: Update, context: CallbackContext) -> None:
    '''
    Wenn man grad einer Lobby gejoint ist, um diese wieder zu verlassen
    '''
    bot = context.bot

    group_chat_id = update.message.chat.id

    try:
        game = games_db.find_game(group_chat_id)

        if (game == None):
            raise Exception("No game found")

        game.remove_player(update.message.from_user.id)

        if (game == None):
            raise Exception("No game found")

        bot.edit_message_text(
            chat_id=group_chat_id,
            text=game.get_player_list_game_text(),
            message_id=game.current_game_msg_id,
            parse_mode=ParseMode.MARKDOWN
        )

    except Exception as e:
        bot.send_message(
            text=str(e),
            chat_id=group_chat_id
        )
        raise e


def new_new_game(update: Update, context: CallbackContext) -> None:
    bot = context.bot

    group_chat_id = update.message.chat.id
    try:
        game = games_db.create_game(
            group_chat_id=group_chat_id,
            roles=" ".join(update.message.text.split(" ")[1:]),
        )

        game.add_player(
            name=update.message.from_user.first_name,
            id=update.message.from_user.id
        )

        new_game_msg_id = bot.sendMessage(
            text=game.get_player_list_game_text(),
            chat_id=group_chat_id,
            parse_mode=ParseMode.MARKDOWN
        )

        game.current_game_msg_id = new_game_msg_id.message_id

    except Exception as e:
        bot.send_message(
            text=str(e),
            chat_id=group_chat_id
        )
        raise e


def new_start_game(update: Update, context: CallbackContext) -> None:
    '''
    Startet das Spiel mit den bisher gejointen Spielern und sendet diesen
    eine DM mit deren zufällig zugeteilten Rolle
    '''
    bot = context.bot
    group_chat_id = update.message.chat.id

    try:
        game = games_db.find_game(group_chat_id)

        if (game == None):
            raise Exception("No game found")

        player_roles = game.distribute_roles()

        for role, players in player_roles.items():
            for player in players:
                # Jedem Spieler seine Rolle mitteilen
                bot.send_message(player.id, f"Du bist {role}")

                # Wenn mehrere Traitor -> andere Traitor mitteilen
                # Außerdem erfahren sie, wer alles Jester ist
                if role == "Traitor":
                    extra_msg = ""

                    # Traitor Kollegen: \n Player1 \n Player2 ...
                    extra_msg += ("Traitor Kollegen:\n" + "\n".join(
                        [p.name for p in players if p != player]) +
                        "\n\n") if len(players) > 1 else ""

                    # Jester: \n Player1 \n Player2 ...
                    extra_msg += (f"Jester:\n" + "\n".join(
                        [p.name for p in player_roles["Jester"]])
                    ) if "Jester" in player_roles else ""

                    if extra_msg.strip() != "":
                        bot.sendMessage(player.id, extra_msg.strip())

    except Exception as e:
        bot.send_message(
            text=str(e),
            chat_id=group_chat_id
        )
        raise e


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
    bot.sendMessage(
        chat_id=update.message.chat.id,
        text=htext,
        parse_mode=ParseMode.MARKDOWN
    )
