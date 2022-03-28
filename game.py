

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


class Player:
    name: str
    id: int

    def __init__(self, name: str, id: int) -> None:
        self.name = name
        self.id = id

    def __repr__(self) -> str:
        return f"{{name: {self.name}, id: {self.id}}}"


class Game:
    players: list[Player] = []
    roles: list[Role] = []
    currentGameMsgId: int = -1

    def __init__(self) -> None:
        pass

    def set_roles(self, input: str) -> None:
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
                f"\"{input}\ doesn't match the required pattern: \n e.g. Traitor:2 Jester:1")

    def set_current_game_msg_id(self, id: int):
        self.currentGameMsgId = id

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

    def __repr__(self) -> str:
        return f"""
        {{
            players: {self.players},
            roles: {self.roles},
            current_game_msg_id: {self.currentGameMsgId}
        }}"""


g1 = Game()
g1.set_roles('Traitor:2 Jester:1z')
g1.add_player("Sebastian", 123)
print(g1)
