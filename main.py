# -*- coding: utf-8 -*-
import gevent
from gevent import monkey;monkey.patch_all()
import sys,signal,logging,argparse
from cfg import *
parse_args()

from cmdclient import Client
from simulator import Simulator

def main():
    if Config["mode"] == "simulator":
        sim = Simulator((Config["host"], Config["port"]))
        sim.run(Config["run"])
    else:
        client = Client()
        client.interact()


if __name__ == "__main__":
    main()
