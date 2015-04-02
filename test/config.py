#### game server address
server = "127.0.0.1"
port   = 8251


############# config proto

##  protobuf
# proto = "protobuf"              # protobuf/sproto
# proto_path = "./data/pb"        # ./data/pb or ./data/sp

## sproto
proto = "sproto"
proto_path = ["./test/test.spb", "./test/test.spb"]
proto_header = "header"

############

########### config mode

## simulator mode
# mode = "simulator"                 # client / simulator
# run = [
#     {
#         "cmd" : "echo",
#         "args" : ["hello world!"],
#         "count" : 1,            # how many clients to launch to run this command
#     },
# ]

## client mode
mode = "client"

############
