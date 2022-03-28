
import random
import math


def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)


def getGroupChatId(update) -> str:
    return str(update.message['chat']['id'])


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


def distribute_roles(players, special_roles) -> dict:
    """
    Return a dict of roles with players e.g.
    {
        'Traitor': ['p7', 'p3'], 
        'Detective': ['p5'], 
        'Unschuldig': ['p8', 'p2', 'p1', 'p6', 'p4']
    }
    """

    # Zufällige Anordnung der Spieler
    rand_players = players[::]
    random.shuffle(rand_players)

    # { role: [p1, p2], role2: [p3, p4, p5] }
    distribution = {}

    # Spezial Rollen verteilen
    for (role, amount) in special_roles.items():

        # Wenn es 1 ist und nicht 1Z oder die random(boolean)
        if (str(amount).isnumeric() == True or bool(random.getrandbits(1))):
            # Z für Zufall, R für Random rausfiltern
            amount = int(''.join(filter(str.isdigit, str(amount))))
            distribution[role] = rand_players[:amount]
            rand_players = rand_players[amount:]

    # remaining belong to innocent
    distribution['Unschuldig'] = rand_players

    return distribution
