import socket, struct, sys
from proto.sproto.sproto import SprotoRpc
import test.config as config

class Handler(object):
    @staticmethod
    def echo(server, msg):
        return msg

class Server(object):
    def __init__(self, addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(addr)
        sock.listen(3)
        self.sock = sock
        self.conn = None

    def _send(self, data):
        self.conn.sendall(struct.pack("!H", len(data)) + data)

    def run(self):
        while True:
            self.conn, addr = self.sock.accept()
            print "accept connection:", addr
            header = self.conn.recv(2, socket.MSG_WAITALL)
            sz, = struct.unpack("!H", header)
            content = self.conn.recv(sz, socket.MSG_WAITALL)
            self.on_recv(content)

    def on_recv(self, content):
        pass

class SprotoServer(Server):
    def __init__(self, port):
        super(SprotoServer, self).__init__(port)
        with open(config.proto_path[0]) as f:
            c2s = f.read()
        with open(config.proto_path[1]) as f:
            s2c = f.read()

        self.proto = SprotoRpc(c2s, s2c, "header")

    def on_recv(self, content):
        p = self.proto.dispatch(content)
        session   = p["session"]
        msg    =    p["msg"]
        protoname = p["proto"]
        assert p["type"] == "REQUEST"
        print "request:", protoname, msg
        resp = getattr(Handler, protoname)(self, msg)
        if session:
            print "response", resp
            pack = self.proto.response(protoname, resp, session)
            self._send(pack)

def main():
    port = config.port
    if len(sys.argv) < 2:
        print "Usage %s [sp/pb]"%sys.argv[0]
        exit()
    if sys.argv[1] == "sp":
        server = SprotoServer(("0.0.0.0", port))
        print "...", server
    else:
        server = PbServer(port)
    print "listen on", port
    server.run()

if __name__ == "__main__":
    main()
