# /usr/bin/python2
# -*- coding: utf-8 -*-
import logging, time, struct
from proto import proto
import gevent
from gevent import socket
from gevent.queue import Queue
from gevent.event import AsyncResult
import socket

from google.protobuf import text_format

import command
from .rc4 import RC4
from cfg import *

class RpcService(object):
    SESSION_ID = 1
    def __init__(self, addr, game):
        self.hub  = gevent.get_hub()
        self.addr = addr
        self.sock = None
        self.game = game

        self.time_diff   = 0

        self.write_queue = Queue()
        self.write_tr    = None

        self.read_queue  = Queue()
        self.read_tr     = None
        self.dispatch_tr = None


        entype = Config.get("encrypt", None)
        if entype == "rc4":
            self.c2s_encrypt = RC4(Config["c2s_key"]).crypt
            self.s2c_encrypt = RC4(Config["s2c_key"]).crypt
        elif entype == None:
            self.c2s_encrypt = None
            self.s2c_encrypt = None
        else:
            raise ValueError("not support %s encrypt"%entype)

        self._sessions = {}

    def _start(self):
        if self.sock:
            return

        # sock = util.RC4Conn(self.addr)
        # sock.connect()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.addr)

        self.sock        = sock
        self.read_tr     = gevent.spawn(self._read)
        self.write_tr    = gevent.spawn(self._write)
        self.dispatch_tr = gevent.spawn(self._dispatch)
        return True

    def set_timestamp(self, timestamp):
        self.time_diff = timestamp - int(time.time())

    def timestamp(self):
        return int(time.time()) + self.time_diff

    def stop(self):
        gevent.spawn(self._stop)

    def _stop(self):
        while True:
            gevent.sleep(1)
            if not self.write_queue.empty():
                continue

            if not self.read_queue.empty():
                continue

            gevent.kill(self.write_tr)
            gevent.kill(self.read_tr)
            gevent.kill(self.dispatch_tr)
            self.sock.close()
            break

    def _write(self):
        while True:
            data = self.write_queue.get()
            if self.c2s_encrypt:
                data = self.c2s_encrypt(data)
            try:
                self.sock.sendall(data)
            except socket.error, e:
                logging.info("write socket failed:%s" % str(e))
                break

    def _read(self):
        left = ""
        while True:
            try:
                buf = self.sock.recv(4*1024)
                if not buf:
                    logging.info("client disconnected, %s:%s" % self.addr)
                    break
                if self.s2c_encrypt:
                    buf = self.s2c_encrypt(buf)

            except socket.error, e:
                logging.info("read socket failed:%s" % str(e))
                break

            left = left + buf
            while True:
                if len(left) < 2:
                   break 

                plen, = struct.unpack('!H', left[:2])
                if len(left) < plen + 2:
                   break 

                data = left[2:plen+2]
                left = left[plen+2:]
                self.read_queue.put(data)

    def _dispatch(self):
        while True:
            data = self.read_queue.get()
            p = proto.dispatch(data)
            session   = p["session"]
            msg    =    p["msg"]

            if p["type"] == "REQUEST":
                protoname = p["proto"]
                cb = command.get_handle(protoname)
                if not cb:
                    print "no handler for proto:", protoname
                    continue
                resp = cb(self.game, msg)
                if session:
                    # rpc call
                    pack = proto.response(protoname, resp, session)
                    self._send(pack)
            else:
                # response
                ev = self._sessions[session]
                del self._sessions[session]
                ev.set(msg)

    def _get_session(self):
        cls = type(self)
        if cls.SESSION_ID > 100000000:
            cls.SESSION_ID = 1
        cls.SESSION_ID += 1
        return cls.SESSION_ID

    def _send(self, data):
        self.write_queue.put(struct.pack("!H", len(data)) + data)

    def invoke(self, protoname, msg):
        pack = proto.request(protoname, msg)
        self._send(pack)

    def call(self, protoname, msg):
        session = self._get_session()
        pack = proto.request(protoname, msg, session)
        ev = AsyncResult()
        self._sessions[session] = ev
        self._send(pack)
        return ev.get()

