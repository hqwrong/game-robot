import sys, os, importlib

cmddir = "cmd"

commands = {}
handles = {}

def _splitargstr(argstr):
    argstr = argstr.strip()
    in_string = None
    j = 0
    delimiter = []
    args = []
    for i in xrange(0, len(argstr)):
        if not delimiter and not in_string and argstr[i] in "\t\n ":
            args.append(argstr[j:i+1])
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

    args.append(argstr[j:i+1])

    return args

def _parseargs(argstr):
    args = _splitargstr(argstr)
    for i in xrange(len(args)):
        args[i] = eval(args[i], {}, {})
    return args
    
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
