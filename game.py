import random

from utilities.core import Task

class Command(object):
    pass

class StartGame(Command):

    def __init__(self, size, players):
        self.size = size
        self.players = players

class MoveDivision(Command):
    pass

class EngageDivision(Command):
    pass

class DestroyDivision(Command):
    pass

class GameOver(Command):

    def __init__(self, winner):
        self.winner = winner

class Game:

    # Constructor {{{1
    def __init__(self, engine):
        self.engine = engine

    # }}}1

    # Game Loop {{{1
    def setup(self):
        self.forum = self.engine.get_forum()
        self.world = self.engine.get_world()

        self.forum.subscribe(StartGame, self.start_game)
        self.forum.subscribe(GameOver, self.game_over)

    def update(self):
        pass

    def teardown(self):
        pass

    # Game Commands {{{1
    def start_game(self, command):
        size = command.size
        players = command.players

        self.world.create_map(size)
        self.world.create_armies(players)

    def game_over(self, command):
        self.world.winner = command.winner
        self.engine.finish()

    # }}}1

class Triggers(Task):

    # Constructor {{{1
    def __init__(self, engine, armies):
        Task.__init__(self, engine)
        self.armies = armies

        self.elapsed = 0
        self.countdown = [1, 2, 3, 4, 5]

    # }}}1

    # Game Loop {{{1
    def setup(self):
        self.world = self.engine.get_world()
        self.forum = self.engine.get_forum()

        self.start_game(self.armies)

    def update(self, time):
        self.elapsed += time

        if self.elapsed > 1:
            print self.countdown.pop()
            self.elapsed = 0

        if not self.countdown:
            self.game_over()

    def teardown(self):
        pass

    # Game Commands {{{1
    def start_game(self, players):

        # Specify how large the map should be.
        size = 100, 100
        width, height = size

        # Give each player a starting position within the map.
        for identity in players:
            name = players[identity]
            position = random.randrange(width), random.randrange(height)

            players[identity] = (name, position)

        command = StartGame(size, players)
        self.forum.publish(command)

    def game_over(self):
        armies = self.world.get_armies()
        winner = random.choice(armies)

        command = GameOver(winner.identity)
        self.forum.publish(command)

    # }}}1

class Player(Task):

    # Constructor {{{1
    def __init__(self, engine, identity):
        Task.__init__(self, engine)
        self.identity = identity

    # }}}1
    
    # Game Loop {{{1
    def setup(self):
        self.world = self.engine.get_world()
        self.forum = self.engine.get_forum()

    def update(self, time):
        pass

    def teardown(self):
        pass

    # }}}1
    # Game Commands {{{1
    # }}}1



