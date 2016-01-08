import socket, struct, sys, time
import StringIO
import threading
import time
import logging

PACKETSIZE=1400
WHOLE=-1
SPLIT=-2

A2S_INFO = ord('T')
A2S_INFO_STRING = 'Source Engine Query'
A2S_INFO_REPLY_OLD = ord('m')
A2S_INFO_REPLY_NEW = ord('I')
A2S_PLAYER = ord('U')
A2S_PLAYER_REPLY = ord('D')
CHALLENGE = -1
S2C_CHALLENGE = ord('A')

IP_BASE_ADDRESS_A = "172.25"

server_list = []

class SourceQueryPacket(StringIO.StringIO):
	# putting and getting values
	def putByte(self, val):
		self.write(struct.pack('<B', val))

	def getByte(self):
		return struct.unpack('<B', self.read(1))[0]

	def putShort(self, val):
		self.write(struct.pack('<h', val))

	def getShort(self):
		return struct.unpack('<h', self.read(2))[0]

	def putLong(self, val):
		self.write(struct.pack('<l', val))

	def getLong(self):
		return struct.unpack('<l', self.read(4))[0]

	def getLongLong(self):
		return struct.unpack('<Q', self.read(8))[0]

	def putFloat(self, val):
		self.write(struct.pack('<f', val))

	def getFloat(self):
		return struct.unpack('<f', self.read(4))[0]

	def putString(self, val):
		self.write(val + '\x00')

	def getString(self):
		val = self.getvalue()
		start = self.tell()
		end = val.index('\0', start)
		val = val[start:end]
		self.seek(end+1)
		return val
	def parsePacket(self):
		header = self.getByte()
		if header == A2S_INFO_REPLY_OLD:
			logging.debug("Parsing map info "+str(self.host))
			result = {}
			result['header'] = chr(A2S_INFO_REPLY_OLD)
			# result['ping'] = after - before
			temp = self.getString()
			result['host_ip'] = self.host
			result['name'] = self.getString()
			result['map'] = self.getString()
			result['folder'] = self.getString()
			result['game'] = self.getString()
			result['numplayers'] = self.getByte()
			result['maxplayers'] = self.getByte()
			result['protocol'] = self.getByte()
			result['server_type'] = chr(self.getByte())
			result['environment'] = chr(self.getByte())
			result['password'] = self.getByte()
			result['mod'] = self.getByte()

			### Too verbose results ###
			# if result['mod'] == 1:
			#     result['link'] = self.getString()
			#     result['download_link'] = self.getString()
			#     self.getByte()
			#     result['version'] = self.getLong()
			#     result['size'] = self.getLong()
			#     result['type'] = self.getByte()
			#     result['dll'] = self.getByte()
			# result['vac'] = self.getByte()
			# result['bots'] = self.getByte()
			return result

		elif header == A2S_INFO_REPLY_NEW:
			# print "Parsing..."
			result = {}
			result['header'] = chr(A2S_INFO_REPLY_NEW)
			# result['ping'] = after - before
			result['host_ip'] = self.host
			result['protocol'] = self.getByte()
			result['name'] = self.getString()
			result['map'] = self.getString()
			result['folder'] = self.getString()
			result['game'] = self.getString()
			self.getByte()
			self.getByte()
			result['numplayers'] = self.getByte()
			result['maxplayers'] = self.getByte()
			result['bots'] = self.getByte()
			result['server_type'] = chr(self.getByte())
			result['environment'] = chr(self.getByte())
			result['password'] = self.getByte()
			result['vac'] = self.getByte()
			result['mod'] = self.getByte()
			return result

		elif header == A2S_PLAYER_REPLY:
			logging.debug("Parsing player info "+str(self.host))
			numplayers = self.getByte()
			result = {}
			result['header'] = chr(A2S_PLAYER_REPLY)
			player_list = []
			# TF2 32player servers may send an incomplete reply
			try:
				for x in xrange(numplayers):
				    player = {}
				    player['ip'] = self.gethost
				    player['index'] = self.getByte()
				    player['name'] = self.getString()
				    player['score'] = self.getLong()
				    player['duration'] = self.getFloat()
				    player_list.append(player)
	  		except Exception, msg:
				logging.error(str(msg))
				return None
			result['player_list'] = player_list
			return result

		elif header == S2C_CHALLENGE:
			self.challenge = self.getLong()
			return self.challenge
		else:
			logging.error("Incorrect header from ip "+str(self.host))

class SourceQueryError(Exception):
	pass

class sendThread (threading.Thread):
	def __init__(self, axlimits, aylimits, udp, port):
		threading.Thread.__init__(self)
		self.axlimits = axlimits
		self.aylimits = aylimits
		self.udp        = udp
		self.port       = port
	def run(self):
		logging.info("Starting Sender Thread")

		spacket = SourceQueryPacket()
		spacket.putLong(WHOLE)
		spacket.putByte(A2S_INFO)
		spacket.putString(A2S_INFO_STRING)

		for i in range (self.axlimits[0],self.axlimits[1]):
			base_ip = IP_BASE_ADDRESS_A+"."+str(i)+"."
			for j in range (self.aylimits[0],self.aylimits[1]):
				current_ip = base_ip + str(j)
				logging.debug("Scanning "+ current_ip)
				try:
					self.udp.sendto(spacket.getvalue(),(current_ip, self.port))
				except socket.error, msg:
					if(msg[0] == 1):
						logging.debug("Sender Error at ip "+ current_ip + " error: " + str(msg))
					else:
						logging.info("Sender Error at ip "+ current_ip + " error: " + str(msg))
					continue
		logging.info("Sender Thread Ended")

class receiverThread (threading.Thread):
	def __init__(self, udp):
		threading.Thread.__init__(self)
		self.udp = udp

	def run(self):
		logging.info("Starting Receiver Thread")
		global server_list
		while True:
			try:
				packet, addr = self.receive()
			except socket.error, msg:
				if msg[0] == 111:                       #Error Connection Refused
					logging.exception("Receiver Error " + str(msg))
				elif str(msg[0]) == "timed out":
					logging.info("Receiver timed out")
					break;
				else:
					logging.exception("Receiver Error " + str(msg))
					continue
			else:
				dat  = packet.parsePacket()
				logging.debug("Parsed map info from "+addr[0])
				server_list.append(dat)
		logging.info("Receiver Thread Ended")

	def receive(self):
		try:
			data, addr = self.udp.recvfrom(PACKETSIZE)
		except socket.error, msg:
			raise
		else:
			logging.info("Data received from" + str(addr))
			packet = SourceQueryPacket(data)
			typ = packet.getLong()

			if typ == WHOLE:
			    logging.debug("Whole Packet")
			    packet.host = addr[0]
			    return packet,addr

			elif typ == SPLIT:
			    # handle split packets
			    logging.debug("Split Packet")
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
				packet.host = addr[0]
				return packet,addr
			    else:
					raise SourceQueryError('Invalid split packet')
			else:
			    raise SourceQueryError("Received invalid packet type %d" % (typ,))

class SourceScanner(object):
	def __init__(self,port=27015, timeout=2.0, axlimits = [1,255], aylimits = [1,255]):
			self.port = port
			self.timeout = timeout
			self.axlimits = axlimits
			self.aylimits = aylimits
			self.udp = False
			self.result = []

	def scanServers(self):

			self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.udp.settimeout(self.timeout)
			self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

			global server_list 
			server_list = []

			rthread = receiverThread(self.udp)
			rthread.start()

			sthread = sendThread(self.axlimits,self.aylimits,self.udp,self.port)
			sthread.start()
			sthread.join()

			rthread.join()

	def scanPlayers(self,ip_list):
		pass
	def getServerList(self):
			global server_list
			return server_list
