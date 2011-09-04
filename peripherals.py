import settings.client
import settings.server

from utilities.core import Task
from utilities.network import EasyServer, EasyClient

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

class ConnectProtocol(Task):
    """ Establishes a connection to the server and gets ready to start the
    game.  One of the primary roles of this class is to receive an id number
    from the server.  This number is used to identify this client for the rest
    of the game. """

    # Constructor {{{1
    def __init__(self, engine):
        Task.__init__(self, engine)

        host = settings.client.host
        port = settings.client.port

        self.client = EasyClient(host, port)

        self.name = settings.client.name
        self.identity = 0

        # Keep track of how much the conversation has progressed, to make sure
        # that it goes in order.
        self.state = 0

    # Attributes {{{1
    def get_name(self):
        return self.name

    def get_identity(self):
        return self.identity

    def get_client(self):
        return self.client

    # }}}1

    # Update Methods {{{1
    def setup(self):
        self.client.outgoing(GiveName, group=self)
        self.client.outgoing(StartPlaying, group=self)

        self.client.incoming(GiveIdentity, self.give_identity, group=self)
        self.client.incoming(StartPlaying, self.start_playing, group=self)

        greeting = GiveName(self.name)

        self.client.queue(greeting)

    def update(self, time):
        self.client.update()

    def teardown(self):
        assert self.identity
        assert self.state == 2

        self.client.forget_group(self)

    # Message Handlers {{{1
    def give_identity(self, pipe, tag, message):
        assert self.state == 0
        self.state = 1

        # Save the identity assigned to this client by the server.
        self.identity = message.identity

    def start_playing(self, pipe, tag, message):
        assert self.state == 1
        self.state = 2

        # Confirm by parroting back the same message.
        pipe.queue(message)

        # Wrap up the pregame and start playing!
        self.engine.finish()

    # }}}1

class AcceptProtocol(Task):
    """ Accepts connections from incoming clients.  Each client is assigned a
    unique id number.  Once enough clients have connected, a message is sent to
    signal the start of the game. """

    # Constructor {{{1
    def __init__(self, engine):
        Task.__init__(self, engine)

        self.seats = 1
        self.playing = 0

        host = settings.server.host
        port = settings.server.port

        self.server = EasyServer(host, port, self.seats, self.greet)

        self.next_id = 1
        self.players = {}

    # Attributes {{{1
    def get_clients(self):
        return self.server.members()

    def get_players(self):
        return self.players

    # }}}1

    # Update Methods {{{1
    def setup(self):
        self.server.setup()

    def update(self, time):
        self.server.accept()
        self.server.update()

    def greet(self, client):
        client.outgoing(GiveIdentity, group=self)
        client.incoming(GiveName, self.give_name, group=self)

        client.outgoing(StartPlaying, group=self)
        client.incoming(StartPlaying, self.start_playing, group=self)

    def teardown(self):
        for client in self.server: client.forget_group(self)
        self.server.teardown()


    # Message Handlers {{{1
    def give_name(self, pipe, tag, message):
        identity = self.next_id; self.next_id += 1
        self.players[identity] = message.name

        greeting = GiveIdentity(identity)
        pipe.queue(greeting)

        if self.server.full():
            message = StartPlaying()
            self.server.broadcast(message)

    def start_playing(self, pipe, tag, message):
        assert self.server.full()
        self.playing += 1

        if self.playing == self.seats:
            self.engine.finish()

    # }}}1

class PregameMenu(Task):
    """ Manages a menu system that allows players to start new games, change
    their settings, and other related actions.  This task also takes care of
    creating a new window. """
    pass

class PostgameMenu(Task):
    """ Displays some statistics about the game that just finished.  Once 
    players leave this mode, they are placed back in the pregame menu. """
    pass

        
