import socket, struct, sys, time
import StringIO
import logging

from source_packet import *

PACKETSIZE = 1400

WHOLE = -1
SPLIT = -2

# A2S_PLAYER
A2S_PLAYER = ord('U')
A2S_PLAYER_REPLY = ord('D')

# S2C_CHALLENGE
CHALLENGE = -1
S2C_CHALLENGE = ord('A')


class PlayerQuery(object):
    """Example usage:
       import SourceQuery
       server = SourceQuery.SourceQuery('1.2.3.4', 27015)
       print server.player()
    """

    def __init__(self, host, port=27015, timeout=3.0):
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

    def player(self):
        # now obtain the actual player info
        try:
            challenge = self.connect(True)
            packet = SourceQueryPacket()
            packet.putLong(WHOLE)
            packet.putByte(A2S_PLAYER)
            packet.putLong(challenge)
        except KeyboardInterrupt:
            logging.error("KeyboardInterrupt exiting...")
            sys.exit(0)
            return []
        except Exception, e:
            logging.error("Error while player query for " + self.host)
            logging.error(str(e))
            return []
        else:
            self.udp.send(packet.getvalue())
            packet = self.receive()

            # this is our player info
            if packet.getByte() == A2S_PLAYER_REPLY:
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

                except Exception, msg:
                    logging.exception(str(msg))
                return result
