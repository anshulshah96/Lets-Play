import StringIO
import struct
import logging 

A2S_INFO = ord('T')
A2S_INFO_STRING = 'Source Engine Query'
A2S_INFO_REPLY_OLD = ord('m')
A2S_INFO_REPLY_NEW = ord('I')
A2S_PLAYER = ord('U')
A2S_PLAYER_REPLY = ord('D')
CHALLENGE = -1
S2C_CHALLENGE = ord('A')

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
			if int(result['mod']) == 1:
			    result['link'] = self.getString()
			    result['download_link'] = self.getString()
			    self.getByte()
			    result['version'] = self.getLong()
			    result['size'] = self.getLong()
			    result['type'] = self.getByte()
			    result['dll'] = self.getByte()
			result['vac'] = self.getByte()
			result['bots'] = self.getByte()
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
				    player['ip'] = self.host
				    player['index'] = self.getByte()
				    player['name'] = self.getString()
				    player['score'] = self.getLong()
				    player['duration'] = self.getFloat()
				    if player['duration'] < 0:		#For handling some exceptional responses
				    	player['duration'] = 0
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