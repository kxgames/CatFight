class World:

    # Constructor {{{1
    def __init__(self):
        self.me = 0
        self.winner = 0

        self.tribes = {}
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

    def get_tribe(self, identity):
        return self.tribes[identity]

    def get_tribes(self):
        return self.tribes.values()

    def get_map(self):
        return self.map

    # }}}1

    # Factory Methods {{{1
    def become(self, identity):
        self.me = identity

    def create_map(self, size):
        self.map = Map(*size)

    def create_tribes(self, players):
        for identity in players:
            name, position = players[identity]

            tribe = Tribe(identity, name, position)
            self.tribes[identity] = tribe

    # }}}1

class Tribe:

    def __init__(self, identity, name, position):
        self.identity = identity
        self.name = name
        self.position = position

class Dot:
    pass

class Map:

    def __init__(self, width, height):
        self.width = width
        self.height = height

