# game-robot

A simple robot client for game server.

## Features

1. multiple proto support, like `sproto` `protobuf`

2. Two modes support. `client` mode for interaction on command line, `simulator` mode for async running which 
   is often used in pressure test.


## Test

Run

    python -m test.server
    
to launch test server

Run

    python main.py test/config.py
    
to launch client.

