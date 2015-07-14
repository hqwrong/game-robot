#!/usr/bin/python2
# -*- coding: utf-8 -*-

from proto.rpcservice import RpcService
from google.protobuf import text_format
import md5, sys, traceback
import gevent

from command import *
from cfg import Config

def _get_secret(uid, token, salt):
    m = md5.new()
    m.update(str(uid))
    m.update(token)
    m.update(salt)
    return m.hexdigest()

class Game(object):
    def __init__(self, addr):
        self.srv = RpcService(addr, self)
        self.is_login = False
        self.uid = None
        self.token = None

        self.srv._start()

    def _dft_handle(self, *args):
        print args
        
    def call(self, protoname, msg = {}):
        return self.srv.call(protoname, msg)

    def send(self, protoname, msg = {}):
        return self.srv.invoke(protoname, msg)

    ################################ Test #########################################
    @addcmd()
    def help(self, cmdname = ""):
        ok,similars = find_cmd(cmdname)
        cmds = [cmdname] if ok else similars
        for cmdname in cmds:
            cmdname,args = inspect_cmd(cmdname)
            print cmdname,args

    @addcmd()
    def login(self, user):
        '''for sproto test login '''
        resp = self.call("login", {"account": user})
        Config["client_prompt"] = "[%s] > " % user
        print(resp["prompt"])

    @addcmd()
    def echo(self, msg):
        '''for sproto echo test '''
        resp = self.call("echo", {"msg" : msg})
        return resp

    @addcmd()
    def addone(self, i):
        self.send("addone", {"i": i})

    @addcmd()
    def addlist(self, l):
        resp = self.call("addlist", {"l": l})
        print "answer:", resp["answer"]

    @addcmd()
    @addhandle("notify_addone")
    def notify_addone(self, i):
        print "addone result:", i
        
    ################################ Test End #########################################
