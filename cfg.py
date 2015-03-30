import argparse,sys

Config = {}

def parse_args():
    parser = argparse.ArgumentParser(description = "New game robot")
    parser.add_argument('-s', '--server', dest = 'host',
                        default = '127.0.0.1', help = 'game server ip address')
    parser.add_argument('-p', '--port', type=int, dest = 'port',
                        default = '8251', help = 'game server tcp port')
    parser.add_argument("-m", '--mode', dest = "mode", choices = ["simulator", "client"])
    parser.add_argument(dest="config", help = "config file")
    args = parser.parse_args()
    if args.config:
        execfile(args.config, Config)
    del args.config

    for k,v in vars(args).iteritems():
        if v:
            Config[k] = v

    sys.path.insert(0, Config["proto_path"])
    
