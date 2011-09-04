class World:

    # Constructor {{{1
    def __init__(self):
        self.me = 0
        self.winner = 0

        self.armies = {}
        self.dots = {}
        self.map = None

    # Attributes {{{1
    def get_me(self):
        return self.me

    def get_winner(self):
        return self.winner

    def is_winner(self):
        if not self.winner: return False
        return self.winner == self.me

    def get_army(self, identity):
        return self.armies[identity]

    def get_armies(self):
        return self.armies.values()

    def get_map(self):
        return self.map

    # }}}1

    # Factory Methods {{{1
    def become(self, identity):
        self.me = identity

    def create_map(self, size):
        self.map = Map(*size)

    def create_armies(self, players):
        for identity in players:
            name, position = players[identity]

            army = Army(identity, name, position)
            self.armies[identity] = army

            # Create divisions and supply lines.

    # }}}1

class Army:

    def __init__(self, identity, name, position):
        self.identity = identity
        self.name = name
        self.position = position

class Division:
    pass

class SupplyLine:
    pass

class Map:

    def __init__(self, width, height):
        self.width = width
        self.height = height

