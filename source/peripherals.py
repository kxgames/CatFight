import settings.client
import settings.server

from utilities.core import Service
from utilities.network import PickleHost, PickleClient

# Connection Protocol Messages {{{1
class GiveName(object):

    def __init__(self, name):
        self.name = name

class GiveIdentity(object):

    def __init__(self, identity):
        self.identity = identity

class StartPlaying(object):
    pass
# }}}1

class ConnectProtocol(Service):
    """ Establishes a connection to the server and gets ready to start the
    game.  One of the primary roles of this class is to receive an id number
    from the server.  This number is used to identify this client for the rest
    of the game. """

    # Constructor {{{1
    def __init__(self, engine):
        Service.__init__(self, engine)

        self.pipe = PickleClient(settings.client.host, settings.client.port)

        self.name = settings.client.name
        self.identity = 0

        # Keep track of how much the conversation has progressed, to make sure
        # that it goes in order.
        self.state = 0

    # Attributes {{{1
    def get_pipe(self):
        return self.pipe

    def get_name(self):
        return self.name

    def get_identity(self):
        return self.identity

    # }}}1

    # Update Methods {{{1
    def setup(self):
        self.pipe.outgoing(GiveName, self.give_name)

        self.pipe.incoming(GiveIdentity, self.give_identity)
        self.pipe.incoming(StartPlaying, self.start_playing)

        greeting = GiveName(self.name)

        self.pipe.setup()
        self.pipe.queue(greeting)

    def update(self, time):
        self.pipe.update()

    def teardown(self):
        assert self.identity
        assert self.state == 3

    # Message Handlers {{{1
    def give_name(self, pipe, message):
        assert self.state == 0
        self.state = 1

    def give_identity(self, pipe, message):
        assert self.state == 1
        self.state = 2

        # Save the identity assigned to this client by the server.
        self.identity = message.identity

    def start_playing(self, pipe, message):
        assert self.state == 2
        self.state = 3

        # Wrap up the pregame and start playing!
        self.engine.finish()

    # }}}1

class AcceptProtocol(Service):
    """ Accepts connections from incoming clients.  Each client is assigned a
    unique id number.  Once enough clients have connected, a message is sent to
    signal the start of the game. """

    # Constructor {{{1
    def __init__(self, engine):
        Service.__init__(self, engine)

        self.host = PickleHost(settings.server.host, settings.server.port)

        self.clients = []
        self.players = {}

        self.next_id = 1
        self.vacancies = 1

    # Attributes {{{1
    def get_clients(self):
        return self.clients

    def get_players(self):
        return self.players

    # }}}1

    # Update Methods {{{1
    def setup(self):
        self.host.setup()

    def update(self, time):
        for client in self.host.accept():
            self.clients.append(client)

            client.outgoing(GiveIdentity)
            client.outgoing(StartPlaying)
            client.incoming(GiveName, self.give_name)

        for client in self.clients:
            client.update()

    def teardown(self):
        message = StartPlaying()

        for client in self.clients:
            client.queue(message)
            client.deliver()

        self.host.teardown()

    # Message Handlers {{{1
    def give_name(self, pipe, message):
        identity = self.next_id; self.next_id += 1
        greeting = GiveIdentity(identity)

        pipe.queue(greeting)

        self.players[identity] = message.name
        self.vacancies -= 1

        # Start the game once enough clients have connected.
        if not self.vacancies:
            self.engine.finish()

    # }}}1

class PregameMenu(Service):
    """ Manages a menu system that allows players to start new games, change
    their settings, and other related actions.  This service also takes care of
    creating a new window. """
    pass

class PostgameMenu(Service):
    """ Displays some statistics about the game that just finished.  Once 
    players leave this mode, they are placed back in the pregame menu. """
    pass

        
