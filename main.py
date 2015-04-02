# -*- coding: utf-8 -*-
import gevent
from gevent import monkey
monkey.patch_all()
monkey.patch_sys()
import sys,signal,logging,argparse
from cfg import *
parse_args()

from cmdclient import Client
from simulator import Simulator

def main():
    srv_addr = (Config["server"], Config["port"])
    print "connect to", srv_addr
    if Config["mode"] == "simulator":
        sim = Simulator(srv_addr)
        sim.run(Config["run"])
    else:
        client = Client(srv_addr)
        client.interact()


if __name__ == "__main__":
    main()
