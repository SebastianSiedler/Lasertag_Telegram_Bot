import random


class Player:
    name: str
    id: int

    def __init__(self, name: str, id: int) -> None:
        self.name = name
        self.id = id

    def __repr__(self) -> str:
        return f"{{name: {self.name}, id: {self.id}}}"


class Role:
    name: str
    quantity: int
    random: bool

    def __init__(self, name: str, quantity: int, random: bool = False) -> None:
        self.name = name
        self.quantity = quantity
        self.random = random

    def __repr__(self) -> str:
        return f"{{name: {self.name}, quantity: {self.quantity}, random: {self.random}}}"


class Game:
    players: list[Player]
    roles: list[Role]
    current_game_msg_id: int
    group_chat_id: int

    def __init__(self, group_chat_id, roles: str) -> None:
        self.group_chat_id = group_chat_id
        self.players = []
        self.roles = []
        self.__set_roles(roles)

    def __set_roles(self, input: str) -> None:
        """
        create roles array from given input string matching 
        the following pattern:\n
        `[roleName]:[quantity][random?]`\n
        e.g. `Traitor:2 Jester:1Z`
        """
        roles = []

        try:
            for role in input.split(" "):
                role_name, role_quantity = role.split(":")

                roles.append(
                    Role(
                        name=role_name,
                        quantity=int(role_quantity.lower().replace("z", "")),
                        random="z" in role_quantity.lower()
                    )
                )
            self.roles = roles

        except:
            raise Exception(
                f"\"{input}\" doesn't match the required pattern: \n e.g. Traitor:2 Jester:1")

    def find_player(self, id: int):
        for player in self.players:
            if player.id == id:
                return player
        return None

    def add_player(self, name: str, id: int):
        if (self.find_player(id) != None):
            raise Exception(f"{name} has already joined!")

        self.players.append(Player(name, id))

    def remove_player(self, id: int):
        player = self.find_player(id)

        if (player == None):
            raise Exception("Player not found")

        self.players.remove(player)

    def distribute_roles(self):
        """
        Return a dict of roles with players e.g.
        ```
        {
            'Traitor': [{name:'p7', id: 7}], 
            'Detective': [{name:'p3', id: 3}], 
            'Unschuldig': [{name:'p6', id: 6}, ...]
        }
        ```
        """

        # Copy players list value
        rand_players = self.players[::]

        # random order of the players
        random.shuffle(rand_players)

        # { role: [p1, p2], role2: [p3, p4, p5] }
        distribution: dict[str, list[Player]] = {}

        # distribute special roles
        for role in self.roles:
            if (role.random == False or bool(random.getrandbits(1))):
                distribution[role.name] = rand_players[:role.quantity]
                rand_players = rand_players[role.quantity:]

        # remaining belong to innocent
        distribution['Unschuldig'] = rand_players

        return distribution

    def get_player_list_game_text(self):
        """
        Erstellt eine Liste aller Spieler.
        z.B.:\n
        *Spieler*:\n
        Player1\n
        Player2\n
        ...
        """
        return ("*Spieler*: \n" + "\n".join([p.name for p in self.players]))

    def __repr__(self) -> str:
        return f"""
        {{
            group_chat_id: {self.group_chat_id},
            players: {self.players},
            roles: {self.roles},
            current_game_msg_id: {self.current_game_msg_id}
        }}"""


class GameDB:
    """
    Contains all currently running games
    """
    games: list[Game] = []

    def find_game(self, group_chat_id: int):
        for game in self.games:
            if game.group_chat_id == group_chat_id:
                return game
        return None

    def create_game(self, group_chat_id, roles: str):
        """
        Erstellt ein neues Spiel und löscht falls vorhanden, das alte
        Spiel der Chat-Gruppe heraus.

        Args:
            roles (str): The text after `/newgame`. e.g. `Traitor:1 Jester:1Z`
        """
        game = self.find_game(group_chat_id)
        if (game != None):
            self.games.remove(game)
            del game

        new_game = Game(group_chat_id, roles)
        self.games.append(new_game)
        return new_game

    def __repr__(self) -> str:
        return ("\n").join([g.__repr__() for g in self.games])
