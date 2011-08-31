import world
import game, peripherals

from utilities.core import SerialEngine, ParallelEngine
from utilities.messaging import ClientBroker, ServerBroker

class ClientPregame(SerialEngine):
    """ Connect to the server, establish the player's identity, and wait for
    the game to start.  The player's identity is passed on to the engine
    responsible for playing the game. """

    def __init__(self, loop):
        SerialEngine.__init__(self, loop)
        self.services = { "protocol" : peripherals.ConnectProtocol(self) }

    def next(self):
        return ClientGame(self.loop, self.services["protocol"])

class ClientGame(SerialEngine):
    """ Play the game over a network.  The client side is only responsible for
    the player on that machine.  Every other game service will be managed by
    the server. """

    def __init__(self, loop, protocol):
        SerialEngine.__init__(self, loop)

        pipe = protocol.get_pipe()
        identity = protocol.get_identity()

        self.world = world.World()
        self.broker = ClientBroker(pipe)
        self.game = game.Game(self)

        self.services = {
                "player" : game.Player(self, identity) }

    def setup(self):
        print "Exiting the client."

    def exit(self):
        return True

class ServerPregame(SerialEngine):
    """ Accept connections from clients until the game is full.  Each player is
    assigned an identity before the game starts. """

    def __init__(self, loop):
        SerialEngine.__init__(self, loop)
        self.services = { "protocol" : peripherals.AcceptProtocol(self) }

    def next(self):
        return ServerGame(self.loop, self.services["protocol"])

class ServerGame(SerialEngine):
    """ Play the game over a network.  The server is responsible for managing
    the computer opponents and any events that aren't explicitly triggered by a
    human player. """

    def __init__(self, loop, protocol):
        SerialEngine.__init__(self, loop)

        clients = protocol.get_clients()
        players = protocol.get_players()

        self.world = world.World()
        self.broker = ServerBroker(clients)
        self.game = game.Game(self)

        self.services = {
                "triggers" : game.Triggers(self, players) }

    def setup(self):
        import time; time.sleep(1)
        print "Exiting the server."

    def exit(self):
        return True
