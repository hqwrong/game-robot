import sys, os, importlib
import inspect

cmddir = "cmd"

commands = {}
handles = {}

def _splitargstr(argstr):
    argstr += " "
    in_string = None
    j = 0
    delimiter = []
    args = []
    for i in xrange(0, len(argstr)):
        if not delimiter and not in_string and argstr[i] in "\t\n ":
            tok = argstr[j:i+1].strip()
            if tok:
                args.append(tok)
                j = i
        elif in_string:
            if argstr[i] == in_string:
                in_string = None
        elif argstr[i] == "'" or argstr[i] == '"':
            in_string = argstr[i]
        elif argstr[i] == "[":
            delimiter.append("]")
        elif argstr[i] == "{":
            delimiter.append("}")
        elif argstr[i] == "]" or argstr[i] == "}":
            if not delimiter or delimiter[-1] != argstr[i]:
                raise NameError("syntax error at %dth char of [%s]"%(i, argstr))
            delimiter.pop()

    if delimiter or in_string:
        raise NameError("syntax error at end of [%s]" % argstr)

    return args

def _parseargs(argstr):
    args = _splitargstr(argstr)
    for i in xrange(len(args)):
        args[i] = eval(args[i], {}, {})
    return args

def find_cmd(cmdname):
    if cmdname in commands:
        return True,[]

    similars = []
    for n in commands:
        if n.startswith(cmdname):
            similars.append(n)

    if not similars:
        mindiff = 100000
        for n in commands:
            d = abs(len(n) - len(cmdname))
            for i in range(min(len(n), len(cmdname))):
                if n[i] != cmdname[i]:
                    d += 1
            if d < mindiff:
                similars = [n]
                mindiff = d
            elif d == mindiff:
                similars.append(n)

    return False, similars

def inspect_cmd(cmdname):
    cmd = commands[cmdname]
    args = inspect.getargspec(cmd["handle"]).args
    del args[0]             # remove `self' arg
    return cmdname, args

def do_cmd(player, cmdname, args):
    cmd = commands[cmdname]
    if callable(cmd["handle"]):
        return cmd["handle"](player, *args)
    else:
        return getattr(player, cmd["handle"], player._dft_handle)(*args)

def do_cmdstr(player, cmdname, argstr):
    cmd = commands[cmdname]
    args = _parseargs(argstr)
    return do_cmd(player, cmdname, args)

def get_handle(protoname):
    return handles.get(protoname, None)



######################## decorators =============================

def addcmd(name = ""):
    def _decorator(f):
        realname = name or f.__name__
        if realname in commands:
            raise NameError(realname)
        commands[realname] = {"name":realname, "handle":f}
        return f

    return _decorator

def addhandle(protoname):
    def _decorator(f):
        if protoname in handles:
            raise NameError(protoname)
        handles[protoname] = f
        return f

    return _decorator

def listcmd():
    return [cmdname for cmdname in commands]

