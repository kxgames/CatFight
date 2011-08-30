from __future__ import division

import pygame, settings
from pygame.locals import *

import settings
import engines

class Loop:
    """ Manage whichever game engine is currently active.  This involves both
    updating the current engine and handling transitions between engines. """

    def play(self):
        clock = pygame.time.Clock()
        frequency = settings.clock_rate

        self.engine.setup()     # All subclasses need to define self.engine.
        self.finished = False

        while not self.finished:
            time = clock.tick(frequency) / 1000
            self.engine.update(time)

            if self.engine.finished():
                self.engine.teardown()
                self.engine = self.engine.next()
                self.engine.setup()

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


