import sys, os, importlib

cmddir = "cmd"

commands = {}
handles = {}

def _parseargs(argtypes, argstr):
    args = argstr.split()
    assert len(args) <= len(argtypes)
    realargs = [None for _ in argtypes]
    for i in range(len(args)):
        t = argtypes[i]
        if t == "string":
            realargs[i] = args[i]
        elif t == "int":
            realargs[i] = int(args[i])
        else:
            raise TypeError(t)
    return realargs
    
def has_cmd(cmdname):
    return cmdname in commands

def do_cmd(player, cmdname, args):
    cmd = commands[cmdname]
    if callable(cmd["handle"]):
        return cmd["handle"](player, *args)
    else:
        return getattr(player, cmd["handle"], player._dft_handle)(*args)

def do_cmdstr(player, cmdname, argstr):
    cmd = commands[cmdname]
    args = _parseargs(cmd["args"], argstr)
    return do_cmd(player, cmdname, args)

def get_handle(protoname):
    return handles.get(protoname, None)



######################## decorators =============================
def addcmd(args = [], name = ""):
    def _decorator(f):
        realname = name or f.__name__
        if realname in commands:
            raise NameError(realname)
        commands[realname] = {"name":realname, "args":args, "handle":f}
        return f

    return _decorator

def addhandle(protoname):
    def _decorator(f):
        if protoname in handles:
            raise NameError(protoname)
        handles[protoname] = f
        return f

    return _decorator
