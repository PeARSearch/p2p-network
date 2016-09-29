#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re
from io import StringIO
import cStringIO
import argparse, socket
import numpy, math
from twisted.internet import reactor
from common_vars import alpha, beta, W
from entangled.node import EntangledNode
from entangled.kademlia.datastore import SQLiteDataStore
from twisted.internet.protocol import Factory, Protocol

node = None

def storeValue(key, value, node):
    """ Stores the specified value in the DHT using the specified key """
    print '\nStoring value; Key: %s, Value: %s' % (key, value)
    # Store the value in the DHT. This method returns a Twisted Deferred result, which we then add callbacks to
    deferredResult = node.iterativeStore(key, value)
    deferredResult.addErrback(genericErrorCallback)

def genericErrorCallback(failure):
    """ Callback function that is invoked if an error occurs during any of the DHT operations """
    print 'An error has occurred:', failure.getErrorMessage()
    reactor.callLater(0, stop)

def stop():
    """ Stops the Twisted reactor, and thus the script """
    print '\nStopping Kademlia node and terminating script...'
    reactor.stop()

def getValue(key):
    """ Retrieves the value of the specified key (KEY) from the DHT """
    global node
    # Get the value for the specified key (immediately returns a Twisted deferred result)
    print '\nRetrieving value from DHT for key "%s"...' % key
    deferredResult = node.iterativeFindValue(key)
    # Add a callback to this result; this will be called as soon as the operation has completed
    deferredResult.addCallback(getValueCallback, key=key)
    # As before, add the generic error callback
    deferredResult.addErrback(genericErrorCallback)
    return deferredResult


def getValueCallback(result, key):
    """ Callback function that is invoked when the getValue() operation succeeds """
    if type(result) == dict:
        print 'Value successfully retrieved: %s' % result[key]
        return result[key]
    else:
        print 'Value not found'
        return None

class PeARSearch(Protocol):
    def dataReceived(self, query_vector):
        query = re.split(r'[\n\r]+', query_vector)
        query_vector = query[-1].strip('"').encode('utf-8')
        q = cStringIO.StringIO(query_vector)
        query_vector = numpy.loadtxt(q)
        query_key = str(lsh(query_vector))
        ret = getValue(key=query_key)
        prot = '/'.join(query[0].split('/')[1:]).strip()
        status = ' 200 OK\n' if ret.result else ' 404 Not Found\n'
        body = ret.result
        length = len(body) if body else 0
        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': length,
            'Connection': 'close',
        }
        response_headers_raw = '\n' + ''.join('%s: %s\n' % (k, v) for k, v in \
                                                response_headers.iteritems())
        response = ''.join([prot, status, response_headers_raw, body or
            ''])
        self.transport.write(response)
        self.transport.loseConnection()

def lsh(vector):
    # TODO: Get the pear profile from the PeARS instance using the TODO API
    alpha.seek(0)
    alpha_array = numpy.loadtxt(alpha)
    lsh_hash = (numpy.dot(alpha_array, vector) + beta)/W
    return int(abs(math.floor(lsh_hash)))

def main(args):
    global node
    arg = parse_arguments(args)
    port = arg.udp_port
    if arg.known_ip and arg.known_port:
        known_nodes = [(arg.known_ip, int(arg.known_port))]
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

    # Set up SQLite-based data store
    if os.path.isfile('/tmp/dbFile%s.db' % sys.argv[1]):
        os.remove('/tmp/dbFile%s.db' % sys.argv[1])
    data_store = SQLiteDataStore(dbFile = '/tmp/db_file_dht%s.db' % port)

    # Generate the Key from the peer profile
    pear_profile = numpy.loadtxt('pear_profile.txt')
    KEY = str(lsh(pear_profile))
    # Bit of a hack. But this return the IP correctly. Just gethostname
    # sometimes returns 127.0.0.1
    VALUE =  ([l for l in ([ip for ip in
        socket.gethostbyname_ex(socket.gethostname())[2] if not
        ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
            s.getsockname()[0], s.close()) for s in
            [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]])
        if l][0][0])

    factory = Factory()
    factory.protocol = PeARSearch
    factory.clients = []
    node = EntangledNode(udpPort=int(port), dataStore=data_store)
    node.joinNetwork(known_nodes)
    reactor.callLater(0, storeValue, KEY, VALUE, node)
    reactor.listenTCP(8080, factory)
    print "Starting the DHT node..."
    reactor.run()

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
    else:
        print "\nNOTE: You have not specified any remote DHT node(s) to connect to."
        print "It will thus not be aware of any existing DHT, but will still "\
                "function as a self-contained DHT (until another node "\
                "contacts it).\n"
    return args

if __name__ == '__main__':
    main(sys.argv[1:])
