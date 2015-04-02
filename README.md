# game-robot

A simple robot client for game server.

## Features

1. multiple proto support, like `sproto` `protobuf`

2. Two modes support. `client` mode for interaction on command line, `simulator` mode for async running which 
   is often used in pressure test.

## Launch
You need a config file to launch. see `test/config.py` for detail.

## Game logic
Please add your logic functions in `game.py`.

use `@addcmd(ARGS, COMMAND_NAME)` decorator to add client command. (Uncomment `mode = "client"` in `test/config.py` to test)

use `@addhandle(protoname)` decorator to add handle function for game server's request.

## Test

To launch test server:

    python -m test/server  sproto
    

To launch client:

    python main.py test/config.py
    

