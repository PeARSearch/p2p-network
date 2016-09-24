import sys
import argparse
import twisted.internet.reactor
from entangled.node import EntangledNode

def main(args):
    arg = parse_arguments(args)
    port = arg.udp_port
    if arg.known_ip and arg.known_port:
        known_nodes = [(arg.known_ip, int(arg.known_node))]
    elif arg.config_file:
        known_nodes = []
        f = open(arg.config_file, 'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            ip_address, udp_port = line.split()
            known_nodes.append((ip_address, int(udp_port)))
    else:
        known_nodes = None
    node = EntangledNode(udpPort=int(port))
    node.joinNetwork(known_nodes)
    print "Starting the DHT node..."
    twisted.internet.reactor.run()

def parse_arguments(args=None):
    usage = "create_network UDP_PORT [KNOWN_NODE_IP  KNOWN_NODE_PORT] "\
    "[-f FILE_WITH_KNOWN_NODES]"
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('udp_port', type=int,
            help="The UDP port that is to be used")
    parser.add_argument('-f', dest='config_file', help="File with known "\
            "nodesit should containg one IP address and UDP port\n"\
            "per line, seperated by a space.", type=argparse.FileType('rt'))
    parser.add_argument('known_ip', help="IP address of the known node"\
                "in the DHT", nargs='?')
    parser.add_argument('known_port', help="Port number of the known node"\
                "in the DHT", type=int, nargs='?')
    args = parser.parse_args()
    if args.known_ip or args.known_port:
        required_together = ('known_port','known_ip')
        if not all([getattr(args,x) for x in required_together]):
            raise RuntimeError("Cannot supply Known Node IP without"\
                " Known IP port")
    return args

if __name__ == '__main__':
    main(sys.argv[1:])
