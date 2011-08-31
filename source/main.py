import engines
import settings.game

from utilities.core import Loop

class UserLoop(Loop):
    """ Run the game.  This main loop can play sandbox games and behave as
    a client in multiplayer games, so it is appropriate for use by the
    end-user. """

    def __init__(self):
        self.engine = engines.ClientPregame(self)

class ServerLoop(Loop):
    """ Manage a network game.  This main loop is responsible for coordinating
    clients in a multiplayer game.  By itself, this is not a complete game. """

    def __init__(self):
        self.engine = engines.ServerPregame(self)


