class Engine:
    """ Control everything happening in the game.  This is just an abstract
    base class providing methods for updating and switching engines.  """

    # Constructor {{{1
    def __init__(self, loop):
        self.loop = loop
        self.complete = False

    # Attributes {{{1
    def get_loop(self):
        return self.loop
    # }}}1

    # Loop Completion {{{1
    def finish(self):
        """ Stop this engine from executing once the current update ends. """
        self.complete = True

    def finished(self):
        """ Return true if this engine is done executing. """
        return self.complete

    def next(self):
        """ Create and return the engine that should be executed next. """
        raise NotImplementedError

    # Loop Methods {{{1
    def setup(self):
        """ Setup the engine.  This is called exactly one time before the first
        update cycle. """
        raise NotImplementedError

    def update(self, time):
        """ Update the engine.  This is called once a frame for as long as the
        engine is running.  The only argument gives the elapsed time since the
        last update. """
        raise NotImplementedError

    def teardown(self):
        """ Tear down the game engine.  This is called after the last update,
        but before the next() method is called to get the next engine. """
        raise NotImplementedError

    # }}}1

class SerialEngine(Engine):
    """ Provide a simple mechanism for executing a set of unrelated services.
    Subclasses are expected to create a dictionary of services called
    self.services.  Every service in that list will be properly handled. """

    def __init__(self, loop):
        Engine.__init__(self, loop)
        self.services = {}

    def get_service(self, name):
        return self.services[name]

    def setup(self):
        for service in self.services.values():
            service.setup()

    def update(self, time):
        for services in self.services.values():
            service.update(time)

    def teardown(self):
        for services in self.services.values():
            service.teardown()

class ParallelEngine(Engine):
    """ Provide a mechanism for executing game services in parallel.  This
    is still an abstract base class, but it allows subclasses to easily
    dispatch tasks into separate threads. """
    pass

class ClientPregame(SerialEngine):
    """ Connect to the server, establish the player's identity, and wait for
    the game to start.  The player's identity is passed on to the engine
    responsible for playing the game. """

    def __init__(self, loop):
        SerialEngine.__init__(self, loop)
        self.services = { "protocol" : services.ConnectProtocol(self) }

    def next(self):
        return ClientGame(self.loop, self.services["protocol"])

class ClientGame(Engine):
    """ Play the game over a network.  The client side is only responsible for
    the player on that machine.  Every other game service will be managed by
    the server. """
    pass

class ServerPregame(Engine):
    """ Accept connections from clients until the game is full.  Each player is
    assigned an identity before the game starts. """

    def __init__(self, loop):
        Engine.__init__(self, loop)
        self.services = { "protocol" : services.AcceptProtocol(self) }

    def next(self):
        return ServerGame(self.loop, self.services["protocol"])

class ServerGame(Engine):
    """ Play the game over a network.  The server is responsible for managing
    the computer opponents and any events that aren't explicitly triggered by a
    human player. """
    pass
