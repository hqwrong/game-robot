# /usr/bin/python2
# -*- coding: utf-8 -*-

from cfg import *

proto = None


if Config["proto"] == "protobuf":
    from .pbproto import PbRpc
    proto = PbRpc(Config["proto_path"])
else:
    from .sproto.sproto import SprotoRpc
    
    with open(Config["proto_path"][0], "rb") as f:
        _c2s_chunk = f.read()
    with open(Config["proto_path"][1], "rb") as f:
        _s2c_chunk = f.read()
    
    proto = SprotoRpc(_c2s_chunk, _s2c_chunk, Config["proto_header"])

