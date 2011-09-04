import world
import game, peripherals

from utilities.core import SerialEngine, ParallelEngine
from utilities.messaging import Forum

class ClientPregame(SerialEngine):
    """ Connect to the server, establish the player's identity, and wait for
    the game to start.  The player's identity is passed on to the engine
    responsible for playing the game. """

    # Constructor {{{1
    def __init__(self, loop):
        SerialEngine.__init__(self, loop)
        self.tasks = { "protocol" : peripherals.ConnectProtocol(self) }

    # Game Loop {{{1
    def successor(self):
        return ClientGame(self.loop, self.tasks["protocol"])

    # }}}1

class ServerPregame(SerialEngine):
    """ Accept connections from clients until the game is full.  Each player is
    assigned an identity before the game starts. """

    # Constructor {{{1
    def __init__(self, loop):
        SerialEngine.__init__(self, loop)
        self.tasks = { "protocol" : peripherals.AcceptProtocol(self) }

    # Game Loop {{{1
    def successor(self):
        return ServerGame(self.loop, self.tasks["protocol"])

    # }}}1


class GameEngine(SerialEngine):
    """ Implements parts of the game loop that are shared between the client
    and the server.  This includes the core game loop. """

    # Constructor {{{1
    def __init__(self, loop):
        SerialEngine.__init__(self, loop)

        self.game = game.Game(self)
        self.world = world.World()
        self.forum = Forum()

    # Attributes {{{1
    def get_world(self):
        return self.world

    def get_forum(self):
        return self.forum

    # }}}1

    # Game Loop {{{1
    def setup(self):
        self.game.setup()
        SerialEngine.setup(self)
        self.forum.lock()

    def update(self, time):
        self.forum.deliver()
        SerialEngine.update(self, time)

        self.forum.deliver()
        self.game.update()

    def teardown(self):
        self.game.teardown()
        SerialEngine.teardown(self)

    # }}}1

class ClientGame(GameEngine):
    """ Plays the game over a network.  The client side is only responsible for
    the player on that machine.  Every other game service will be managed by
    the server. """

    # Constructor {{{1
    def __init__(self, loop, protocol):
        GameEngine.__init__(self, loop)

        client = protocol.get_client()
        identity = protocol.get_identity()

        self.forum.connect(client)
        self.world.become(identity)

        self.tasks = {
                "player" : game.Player(self, identity) }

    # Game Loop {{{1
    def successor(self):
        return ClientPostgame(self.loop, self.world)

    # }}}1

class ServerGame(GameEngine):
    """ Plays the game over a network.  The server is responsible for managing
    the computer opponents and any events that aren't explicitly triggered by a
    human player. """

    # Constructor {{{1
    def __init__(self, loop, protocol):
        GameEngine.__init__(self, loop)

        clients = protocol.get_clients()
        players = protocol.get_players()

        self.forum.connect(*clients)
        self.tasks = {
                "triggers" : game.Triggers(self, players) }

    # Game Loop {{{1
    def successor(self):
        return ServerPostgame(self.loop)

    # }}}1


class ClientPostgame(SerialEngine):

    def __init__(self, loop, world):
        SerialEngine.__init__(self, loop)
        self.world = world

    def setup(self):
        print "You win!" if self.world.is_winner() else "You lose."

    def exit(self):
        return True

class ServerPostgame(SerialEngine):

    def setup(self):
        import time; time.sleep(0.2)
        print "Exiting server."

    def exit(self):
        return True

