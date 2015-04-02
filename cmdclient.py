import sys
from game import Game
from command import do_cmdstr,has_cmd


ROBOT_CLIENT_PROMPT = "> "

class Client(object):
    def __init__(self, srv_addr):
        self.game = Game(srv_addr)

    def interact(self):
        while True:
            try:
                sys.stdout.write(ROBOT_CLIENT_PROMPT)
                sys.stdout.flush()

                l = sys.stdin.readline().strip()
                tokens = l.split(None, 1)
                if not tokens:
                    continue
                cmdname = tokens[0]
                if not has_cmd(cmdname):
                    print("cmd not found:", cmdname)
                    continue
                result = do_cmdstr(self.game, cmdname, tokens[1] if len(tokens) > 1 else "")
                if result != None:
                    print(result)

            except KeyboardInterrupt:
                print "keyboard Interrupted."
                break

            except:
                raise
                
