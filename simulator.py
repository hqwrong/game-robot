import gevent
import command
from game import Game

def _print():
    print "hello"

class Simulator(object):
    def __init__(self, srv_addr):
        self.srv_addr = srv_addr
        self.workers = []

    def run(self, actorlist):
        for actor in actorlist:
            assert command.has_cmd(actor["cmd"]),actor["cmd"]
            for _ in xrange(actor.get("count", 1)):
                self.workers.append(gevent.spawn(command.do_cmd, Game(self.srv_addr), actor["cmd"], actor["args"]))

        gevent.wait(self.workers)
