import gevent
from gevent import monkey
monkey.patch_all()
import socket, struct, sys
from proto.sproto.sproto import SprotoRpc
import test.config as config
from test.rc4 import RC4

class Handler(object):
    @staticmethod
    def echo(server, msg):
        return msg

    @staticmethod
    def addone(server, msg):
        server.send("notify_addone", {"i":msg["i"]+1})

    @staticmethod
    def login(server, msg):
        return {"prompt": "hello, %s"%msg["account"]}

    @staticmethod
    def addlist(server, msg):
        accum = 0
        for i in msg["l"]:
            accum += i
        return {"answer": accum}

class GameServer(object):
    def __init__(self, conn, addr):
        self.conn = conn
        self.client_addr = addr
        self.c2s_encrypt = None
        self.s2c_encrypt = None

        with open(config.proto_path[0]) as f:
            c2s = f.read()
        with open(config.proto_path[1]) as f:
            s2c = f.read()

        self.proto = SprotoRpc(c2s, s2c, "header")

        self._init_encrypt()

    def _init_encrypt(self):
        entype = getattr(config, "encrypt", None)
        if entype == "rc4":
            self.c2s_encrypt = RC4(config.c2s_key).crypt
            self.s2c_encrypt = RC4(config.s2c_key).crypt
        elif entype == None:
            self.c2s_encrypt = None
            self.s2c_encrypt = None
        else:
            raise ValueError("not support %s encrypt"%entype)

    def _send(self, data):
        data = struct.pack("!H", len(data)) + data
        if self.s2c_encrypt:
            data = self.s2c_encrypt(data)
        self.conn.sendall(data)

    def _recv(self, sz):
        data = self.conn.recv(sz, socket.MSG_WAITALL)
        if self.c2s_encrypt:
            data = self.c2s_encrypt(data)
        return data

    def run(self):
        while True:
            header = self._recv(2)
            if not header:
                print "disconnected", self.client_addr
                break
            sz, = struct.unpack("!H", header)
            content = self._recv(sz)
            p = self.proto.dispatch(content)
            session   = p.get("session", 0)
            msg    =    p["msg"]
            protoname = p["proto"]
            assert p["type"] == "REQUEST"
            print "request:", protoname, msg
            resp = getattr(Handler, protoname)(self, msg)
            if session:
                print "response", resp
                pack = self.proto.response(protoname, resp, session)
                self._send(pack)

    def send(self, protoname, msg):
        pack = self.proto.request(protoname, msg)
        self._send(pack)


class Server(object):
    def __init__(self, addr, prototype):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addr)
        sock.listen(3)
        self.sock = sock
        self.conn = None

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            gs = GameServer(conn, addr)
            gevent.spawn(gs.run)

def main():
    port = config.port
    if len(sys.argv) < 2:
        print "Usage %s [sproto/protobuf]"%sys.argv[0]
        exit()
    server = Server(("0.0.0.0", port), sys.argv[1])
    print "listen on", port
    server.run()

if __name__ == "__main__":
    main()
