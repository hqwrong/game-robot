# game-robot

A simple robot client for game server.

## Features

1. Multiple protos support. `sproto` and `protobuf` so far.

2. Two modes support. `client` mode for interaction on command line, `simulator` mode for async running which 
   is often used in pressure test.

## Setup && Launch

Run

    git submodule update --init --recursive

after first clone.

Run

    make

to build.

You need a config file to launch. see `test/config.py` for detail.

## Game logic
Please add your logic functions to `game.py`.

use `@addcmd(ARGS, COMMAND_NAME)` decorator to add client command. (uncomment `mode = "client"` in `test/config.py` to test)

use `@addhandle(protoname)` decorator to add handle function for game server's request.

## Test

To launch test server:

    python -m test/server  sproto
    

To launch client:

    python main.py test/config.py

Now you've got a client to interact, try to type `addone 1` or `echo hello` to play around.

