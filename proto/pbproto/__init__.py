import os, sys, time
from . import proto_dict
import client_rpc
from .protobuf_to_dict import protobuf_to_dict, dict_to_protobuf

def _pb2dict(msg):
    return protobuf_to_dict(msg, use_enum_labels=True)

def _dict2pb(pb, values):
    return dict_to_protobuf(pb, values)

class Message(object):
    def __init__(self, pack, id):
        self.__dict__['_Rpc_Pack'] = pack 
        self.__dict__['_Rpc_Type_Id'] = id

    def __getattr__(self, key):
        if key not in ('_Rpc_Pack', '_Rpc_Type_Id'):
            return getattr(self._Rpc_Pack, key)
        if key == '_Rpc_Type_Id':
            return self.__dict__['_Rpc_Type_Id']
        else:
            raise AttributeError

    def __setattr__(self, key, value):
        if key not in ('_Rpc_Pack', '_Rpc_Type_Id'):
            setattr(self._Rpc_Pack, key, value)
        else:
            raise AttributeError

    def type_id(self):
        return self.__dict__['_Rpc_Type_Id']

    def pb_pack(self):
        return self.__dict__['_Rpc_Pack']

    def encode(self):
        return self.__dict__['_Rpc_Pack'].SerializeToString()

    def decode(self, data):
        return self.__dict__['_Rpc_Pack'].ParseFromString(data)
    

class PbRpc(object):
    def __init__(self, pb_path):
        self._handlers = {}
        self._name2id = {}
        self._module2name = {}
        self._sessions = {}
        self.time_diff   = 0

        proto_dict.load_dir(pb_path)
        self.__register_message(client_rpc.Descriptor)

    def __register_message(self, descriptor):
        for module_name in descriptor:
            name_list = []
            for desc in descriptor[module_name]:
                name = desc['name']
                type_name = module_name + '.' + desc['name']
                handler = {
                        'input' : proto_dict.get(desc['input']),
                        'output': proto_dict.get(desc['output']),
                        'id': desc['id'],
                        'name':  type_name,
                        'module_name': module_name,
                        }
                self._handlers[desc['id']] = handler
                self._name2id[type_name] = desc['id']
                name_list.append(name)
            self._module2name[module_name] = name_list

    def parse_pack(self, pack):
        p = proto_dict.get('proto.Pack')()
        p.ParseFromString(pack)
        return p

    def pack(self, session = None, type = None, body = None, timestamp = None):
        p = proto_dict.get('proto.Pack')()
        if session != None:
            p.session = session
        if type != None:
            p.type = type
        if body != None:
            p.data = body
        if timestamp != None:
            p.timestamp = timestamp
        else:
            p.timestamp = int(time.time() - 2.5)

        return p.SerializeToString()

    def lookup(self, type_name, input = True):
        handler = self._handlers[self._name2id[type_name]]
        if input:
            message = Message(handler['input'](), handler['id'])
        else:
            message = Message(handler['output'](), handler['id'])

        return message

    def type_name(self, type_id):
        return self._handlers[type_id]["name"]

    def type_names(self, module_name):
        return self._module2name[module_name]

    def type_id(self, type_name):
        return self._name2id[type_name]

    def module_name(self, type_id):
        return self._handlers[type_id]["module_name"]

    def has_response(self, type_id):
        return self._handlers[type_id]["output"] and True or False

    def parse_pack(self, pack):
        p = proto_dict.get('proto.Pack')()
        p.ParseFromString(pack)
        return p

    def set_timestamp(self, timestamp):
        self.time_diff = timestamp - int(time.time())

    def timestamp(self):
        return int(time.time()) + self.time_diff

    def make_pack(self, msg, pack):
        def _fill(msg, pack, depth = 0):
            if depth > 100:
                raise OverflowError("too deep")

            if type(msg) is dict:
                for k,v in msg.iteritems():
                    if type(v) != dict and type(v) != list:
                        setattr(pack, k, v)
                    else:
                        _fill(v, getattr(pack,k), depth+1)
            elif type(msg) is list:
                for v in msg:
                    if type(v) != dict and type(v) != list:
                        pack.add(v)
                    else:
                        _fill(v, pack.add(), depth+1)
            else:
                raise TypeError(type(msg))

        return _fill(msg, pack)

    def dispatch(self, data):
        p = self.parse_pack(data)
        if p.type != 0:
            # request
            type_id = p.type
            type_name = self.type_name(type_id)
            message = self.lookup(type_name)
            message.decode(p.data)
            return {
                "type":"REQUEST", 
                "proto":type_name, 
                "msg": _pb2dict(message),
                "session": p.session if p.session != 0 else None,
            }
        else:
            # response
            session = p.session
            type_name = self._sessions[session]
            message = self.lookup(type_name, False)
            message.decode(p.data)
            del self._sessions[session]
            return {"type":"RESPONSE", "session":session, "msg":_pb2dict(message)}
        
    def request(self, protoname, msg, session = 0):
        if session:
            self._sessions[session] = protoname
        pack = self.lookup(protoname)
        if msg:
            _dict2pb(pack.pb_pack(), msg)

        return self.pack(session, pack.type_id(), pack.encode(), self.timestamp())
        
    def response(self, protoname, msg, session):
        pack = self.lookup(protoname)
        if msg:
            _dict2pb(pack.pb_pack(), msg)
        return self.pack(session, pack.type_id(), pack.encode(), self.timestamp())
