import sys,traceback
from game import Game
from command import do_cmdstr,find_cmd

import pprint

from cfg import Config


class Client(object):
    def __init__(self, srv_addr):
        self.game = Game(srv_addr)

    def docmd(self, tokens):
        cmdname = tokens[0]
        ok,similars = find_cmd(cmdname)
        if not ok:
            print "cmd not found:", cmdname
            print "Did you mean this?"
            print "\t", ", ".join(similars)
            return
        result = do_cmdstr(self.game, cmdname, tokens[1] if len(tokens) > 1 else "")
        if result != None:
            pprint.pprint(result)
    
    def interact(self):
        if "uid" in Config:
            self.docmd(["login", Config["uid"]])
        while True:
            try:
                sys.stdout.write(Config["client_prompt"])
                sys.stdout.flush()
                l = sys.stdin.read(1)
                if not l: # eof
                    print "exit on EOF"
                    exit(0)
                if l == '\n':
                    continue
                l += sys.stdin.readline()
                l.strip()
                tokens = l.split(None, 1)
                if not tokens:
                    continue
                self.docmd(tokens)

            except Exception as e:
                print "error occured", e, traceback.format_exc()
                continue
