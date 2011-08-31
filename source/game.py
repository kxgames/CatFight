from utilities.core import Service

class Command(object):
    pass

class StartGame(Command):
    pass

class CreateDot(Command):
    pass

class MoveDot(Command):
    pass

class DestroyDot(Command):
    pass

class DestroyPlayer(Command):
    pass

class StopGame(Command):
    pass

class Game:

    def __init__(self, engine):
        self.engine = engine

class Manager(Service):
    pass

class Triggers(Manager):

    def __init__(self, engine, players):
        Manager.__init__(self, engine)

class Player(Manager):

    def __init__(self, engine, identity):
        Manager.__init__(self, engine)
        self.identity = identity


