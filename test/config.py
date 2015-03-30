# proto = "protobuf"              # protobuf/sproto
# proto_path = "./data/pb"       # ./data/pb or ./data/sp

proto = "sproto"
proto_path = ["./test/test.spb", "./test/test.spb"]
proto_header = "header"

mode = "simulator"                 # client / simulator
server = "127.0.0.1"
port   = 8251
run = [
    {
        "cmd" : "echo",
        "args" : ["hello world!"],
        "count" : 1,
    },
]
