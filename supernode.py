from twisted.internet import reactor, protocol
import sqlite3

GETPORT = 9000
POSTPORT = 9001
conn = sqlite3.connect('super_db.sqlite')
c = conn.cursor()

# Class that takes care of supernode data store
class SupernodePost(protocol.Protocol):
    def dataReceived(self, data):
        node_data = re.split(r'[\n\r]+', data)
        port = query[-1].strip('"').encode('utf-8')
        ip = query[0].strip('"').encode('utf-8')
        c.execute("INSERT INTO supernode VALUES ({},{})".format(ip, port))
        conn.commit()

class SupernodePostFactory(protocol.Factory):
        protocol = SupernodePost


# Class that takes care of supernode lookup
class SupernodeGet(protocol.Protocol):
    def dataLookup(self, data):
        ports = []
        node_data = re.split(r'[\n\r]+', data)
        ip = query[-1].strip('"').encode('utf-8')
        t = (ip,)
        for row in c.execute('SELECT * FROM supernode WHERE ip=?', t):
            ports.append(row(-1))
        self.transport.write(ports)


class SupernodeGetFactory(protocol.Factory):
    def buildProtocol(self, data):
        return SupernodeGet()


store_factory = SupernodeGetFactory()
lookup_factory = SupernodePostFactory()
reactor.listenTCP(GETPORT, store_factory)
reactor.listenTCP(POSTPORT, lookup_factory)
reactor.run()
conn.close()
