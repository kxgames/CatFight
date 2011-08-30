#!/usr/bin/env python

import main
import multiprocessing

class DebuggingProcess(multiprocessing.Process):
    """ Wrap one of the main loops so that it can be executed in a background
    process.  This makes it much easier to simulate network games. """

    def __init__(self, name, loop):
        multiprocessing.Process.__init__(self, name=name)
        self.loop = loop

    def __nonzero__(self):
        return self.is_alive()

    def run(self):
        self.loop.play()

if __name__ == "__main__":

    threads = [
            DebuggingProcess("Client", main.UserLoop()),
            DebuggingProcess("Server", main.ServerLoop()) ]

    try:
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        pass

