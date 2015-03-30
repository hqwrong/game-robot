#!/usr/bin/python2
# -*- coding: utf-8 -*-

from proto.rpcservice import RpcService
from google.protobuf import text_format
import md5, sys, traceback
import gevent

from command import *

def _get_secret(uid, token, salt):
    m = md5.new()
    m.update(str(uid))
    m.update(token)
    m.update(salt)
    return m.hexdigest()

class Game(object):
    def __init__(self, addr):
        self.srv = RpcService(addr)
        self.is_login = False
        self.uid = None
        self.token = None

        self.srv._start()

    def _dft_handle(self, *args):
        print args
        
    def call(self, protoname, msg):
        return self.srv.call(protoname, msg)

    def send(self, protoname, msg):
        return self.srv.invoke(protoname, msg)

    ################################ Test #########################################
    @addhandle("test")
    def test(self, args):
        print("receive test notify", args)


    @addcmd(["int", "string"])
    def login(self, uid, token):
        self.uid = uid
        self.token = token or "for_cmd_client"
        resp = self.call("client.check_version", {"client_version" : "I'm a robot!"})
        if resp.code != 0:
            return "uid: %d check version failed, errcode:%d" % (self.uid, resp.errcode)

        self.salt = resp.salt
        pack = {
            "uid": self.uid,
            "token": _get_secret(self.uid, self.token, self.salt),
        }
        resp = self.call("client.login", pack)
        if resp.errcode != 0:
            return "uid: %d login failed, errcode:%d" % (self.uid, resp.errcode)

        # self.srv.set_timestamp(resp.timestamp)
        self.is_login = True
        print("uid: %d login succeed" % self.uid)

        return None

    @addcmd(name = "create")
    def create_user(self):
        resp = self.call("client.create", {"platform" : 1})
        print resp.uid, resp.token

    @addcmd()
    def login2(self):
        '''for sproto test login '''
        resp = self.call("login", {"account": "test_account"})
        print("response:", resp)
        return resp

    @addcmd(["string"])
    def echo(self, msg):
        '''for sproto echo test '''
        resp = self.call("echo", {"msg" : msg})
        print("response:", resp)
        return resp
        
    ################################ Test End #########################################
