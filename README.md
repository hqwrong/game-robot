# game-robot

A simple robot client for game server.

## Features

1. Provide high level synchronous api based on [gevent](http://gevent.org/)

2. Multiple protos support. [sproto](https://github.com/cloudwu/sproto) and [protobuf](https://github.com/google/protobuf) so far.

3. Two modes support. `client` mode for interaction on command line, `simulator` mode for async running which is often used in pressure test.

3. simple and easy-to-use api. Actually, you only have to put a decorator(@addcmd or @handle) above your function to make it a client command or a handle for proto request.

4. simple but powerful command client, which support passing in types of string, int, list and dict.

5. stream encrypt support built in.

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

use `@addcmd(ARGS, COMMAND_NAME)` decorator to add client command.

use `@addhandle(protoname)` decorator to add handle function for game server's request.

## Test

### test cmdclient
To launch test server:

    python -m test/server  sproto
    
To launch client:

    python main.py test/config.py

Now you've got a client to play with:

    $ python2 main.py test/config.py
    connect to ('127.0.0.1', 8251)
    > login "foobar"
    hello, foobar
    [foobar] > addlist [1,3,5,7]
    answer: 16
    [foobar] > echo "hello"
    {'msg': 'hello'}

### test simulator
To launch test server:

    python -m test/server  sproto

Uncomment following block in test/config.py:

    mode = "simulator"                 # client / simulator
    run = [
        {
            "cmd" : "echo",
            "args" : ["hello world!"],
            "count" : 5,            # how many clients to launch to run this command
        },
        {
            "cmd": "addlist",
            "args" : [ [1,2,3,4,5] ],
            "count" : 3,
        }
    ]

Run client to run:
    python main.py test/config.py
