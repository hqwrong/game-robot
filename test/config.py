############# game server address
server = "127.0.0.1"
port   = 8251

############# stream encrypt
encrypt = "rc4"
c2s_key = "C2S_RC4"
s2c_key = "S2C_RC4"

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

## client mode
mode = "client"

# mode = "simulator"                 # client / simulator
# run = [
#     {
#         "cmd" : "echo",
#         "args" : ["hello world!"],
#         "count" : 5,            # how many clients to launch to run this command
#     },
#     {
#         "cmd": "addlist",
#         "args" : [[1,2,3,4,5]],
#         "count" : 3,
#     }
# ]

############
