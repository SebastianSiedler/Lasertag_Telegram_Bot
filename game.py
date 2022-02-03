import random





def distribute_roles(players, SPECIAL_ROLES) -> dict:
    """
    Return a dict of roles with players e.g.
    {
        'Traitor': ['p7', 'p3'], 
        'Detective': ['p5'], 
        'Unschuldig': ['p8', 'p2', 'p1', 'p6', 'p4']
    }
    """

    # SPECIAL_ROLES = {
    #     'Traitor': 0.25,
    #     'Detective': 0.125,
    #     'SpezialRolle2': 0.125
    # }

    # Zufällige Anordnung der Spieler
    rand_players = players[::]
    random.shuffle(rand_players)

    # { role: [p1, p2], role2: [p3, p4, p5] }
    distribution = {}

    # Spezial Rollen verteilen
    for (role, amount) in SPECIAL_ROLES.items():

        # Wenn es 1 ist und nicht 1Z oder die random(boolean)
        if (str(amount).isnumeric() == True or bool(random.getrandbits(1))):
            # Z für Zufall, R für Random rausfiltern
            amount = int(''.join(filter(str.isdigit, str(amount))))
            distribution[role] = rand_players[:amount]
            rand_players = rand_players[amount:]

    # remaining belong to innocent
    distribution['Unschuldig'] = rand_players

    return distribution
