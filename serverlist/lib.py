"""http://developer.valvesoftware.com/wiki/Server_Queries"""
import socket, struct, sys, time
import StringIO
from serverlist.maplib import *

PACKETSIZE=1400

WHOLE=-1
SPLIT=-2

A2S_INFO = ord('T')
A2S_INFO_STRING = 'Source Engine Query'
A2S_INFO_REPLY = ord('I')

# A2S_PLAYER
A2S_PLAYER = ord('U')
A2S_PLAYER_REPLY = ord('D')

# A2S_RULES
A2S_RULES = ord('V')
A2S_RULES_REPLY = ord('E')

# S2C_CHALLENGE
CHALLENGE = -1
S2C_CHALLENGE = ord('A')

class SourceQueryError(Exception):
    pass

class SourceQuery(object):
    """Example usage:
       import SourceQuery
       server = SourceQuery.SourceQuery('1.2.3.4', 27015)
       print server.ping()
       print server.info()
       print server.player()
       print server.rules()
    """

    def __init__(self, host, port=27015, timeout=1.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.udp = False

    def disconnect(self):
        if self.udp:
            self.udp.close()
            self.udp = False

    def connect(self, challenge=False):
        self.disconnect()
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.settimeout(self.timeout)
        self.udp.connect((self.host, self.port))

        if challenge:
            return self.challenge()

    def receive(self):
        packet = SourceQueryPacket(self.udp.recv(PACKETSIZE))
        typ = packet.getLong()

        if typ == WHOLE:
            return packet

        elif typ == SPLIT:
            # handle split packets
            reqid = packet.getLong()
            total = packet.getByte()
            num = packet.getByte()
            splitsize = packet.getShort()
            result = [0 for x in xrange(total)]

            result[num] = packet.read()

            # fetch all remaining splits
            while 0 in result:
                packet = SourceQueryPacket(self.udp.recv(PACKETSIZE))

                if packet.getLong() == SPLIT and packet.getLong() == reqid:
                    total = packet.getByte()
                    num = packet.getByte()
                    splitsize = packet.getShort()
                    result[num] = packet.read()

                else:
                    raise SourceQueryError('Invalid split packet')

            packet = SourceQueryPacket("".join(result))

            if packet.getLong() == WHOLE:
                return packet

            else:
                raise SourceQueryError('Invalid split packet')

        else:
            raise SourceQueryError("Received invalid packet type %d" % (typ,))

    def ping(self):
        """Deprecated. Use info()['ping'] instead."""
        return self.info()['ping']

    def challenge(self):
        # use A2S_PLAYER to obtain a challenge
        packet = SourceQueryPacket()
        packet.putLong(WHOLE)
        packet.putByte(A2S_PLAYER)
        packet.putLong(CHALLENGE)

        self.udp.send(packet.getvalue())
        packet = self.receive()

        # this is our challenge packet
        if packet.getByte() == S2C_CHALLENGE:
            challenge = packet.getLong()
            return challenge
            
    def info(self):
        """Return a dict with server info and ping."""
        self.connect()

        packet = SourceQueryPacket()
        packet.putLong(WHOLE)
        packet.putByte(A2S_INFO)
        packet.putString(A2S_INFO_STRING)

        before = time.time()

        self.udp.send(packet.getvalue())
        packet = self.receive()

        after = time.time()
        # print "Checking..."
        header = packet.getByte()
        if header == 109:
            # print "Parsing..."
            result = {}
            result['header'] = "m"
            result['ping'] = after - before
            result['hostname'] = packet.getString()
            result['name'] = packet.getString()
            result['map'] = packet.getString()
            result['folder'] = packet.getString()
            result['game'] = packet.getString()
            result['numplayers'] = packet.getByte()
            result['maxplayers'] = packet.getByte()
            result['protocol'] = packet.getByte()
            result['server_type'] = chr(packet.getByte())
            result['environment'] = chr(packet.getByte())
            result['password'] = packet.getByte()
            result['mod'] = packet.getByte()
            result['vac'] = None

            ### Too verbose results ###
            # if result['mod'] == 1:
            #     result['link'] = packet.getString()
            #     result['download_link'] = packet.getString()
            #     packet.getByte()
            #     result['version'] = packet.getLong()
            #     result['size'] = packet.getLong()
            #     result['type'] = packet.getByte()
            #     result['dll'] = packet.getByte()
            # result['vac'] = packet.getByte()
            # result['bots'] = packet.getByte()
            
            return result

        elif header == 73:
            # print "Parsing..."
            result = {}
            result['header'] = "I"
            result['ping'] = after - before
            result['hostname'] = self.host
            result['protocol'] = packet.getByte()
            result['name'] = packet.getString()
            result['map'] = packet.getString()
            result['folder'] = packet.getString()
            result['game'] = packet.getString()
            packet.getByte()
            packet.getByte()
            result['numplayers'] = packet.getByte()
            result['maxplayers'] = packet.getByte()
            result['bots'] = packet.getByte()
            result['server_type'] = chr(packet.getByte())
            result['environment'] = chr(packet.getByte())
            result['password'] = packet.getByte()
            result['vac'] = packet.getByte()
            result['mod'] = packet.getByte()
            return result

    def player(self):
        challenge = self.connect(True)

        # now obtain the actual player info
        packet = SourceQueryPacket()
        packet.putLong(WHOLE)
        packet.putByte(A2S_PLAYER)
        packet.putLong(challenge)

        self.udp.send(packet.getvalue())
        packet = self.receive()

        # this is our player info
        # print "Checking Info..."
        if packet.getByte() == A2S_PLAYER_REPLY:
            # print "Parsing..."
            numplayers = packet.getByte()
            result = []
            # TF2 32player servers may send an incomplete reply
            try:
                for x in xrange(numplayers):
                    player = {}
                    player['index'] = packet.getByte()
                    player['name'] = packet.getString()
                    player['score'] = packet.getLong()
                    player['duration'] = packet.getFloat()
                    result.append(player)
            except:
                pass

            return result

    def rules(self):
        challenge = self.connect(True)

        # now obtain the actual rules
        packet = SourceQueryPacket()
        packet.putLong(WHOLE)
        packet.putByte(A2S_RULES)
        packet.putLong(challenge)

        self.udp.send(packet.getvalue())
        packet = self.receive()

        # this is our rules
        if packet.getByte() == A2S_RULES_REPLY:
            rules = {}
            numrules = packet.getShort()

            # TF2 sends incomplete packets, so we have to ignore numrules
            while 1:
                try:
                    key = packet.getString()
                    rules[key] = packet.getString()
                except:
                    break

            return rules
