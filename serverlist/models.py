from django.db import models

class Player(models.Model):
	name = models.CharField(max_length=200)
	duration = models.IntegerField(default=0)
	score = models.IntegerField(default=0)
	def __str__(self):
		return self.name

class Server(models.Model):
	ip = models.CharField(max_length=200)			#Ex. 172.25.12.131
	map_name = models.CharField(max_length=200)		#Ex. rush
	server_name = models.CharField(max_length=200)	#Ex. Exams Over B**ch!
	game_name = models.CharField(max_length=200,default="Counter-Strike 1.6")	#Ex. Counter-Strike 1.6
	host = models.CharField(max_length=200)			#Ex. 172.25.12.131:27015
	num_players = models.IntegerField(default=0)	
	max_players = models.IntegerField(default=0)
	num_bots = models.IntegerField(default=0)
	folder = models.CharField(max_length=200)
	environment = models.CharField(max_length=200,default = "Windows")		# w-Windows,l-Linux,m/o-Mac
	password_protected = models.CharField(max_length=10,default = "No")	#0 for public, 1 for private
	vac_secured = models.NullBooleanField(default=False)		#0 for unsecured, 1 for secured
	folder = models.CharField(max_length=200,default="None")
	server_type = models.CharField(max_length=200,default="None")	
	protocol = models.CharField(max_length=200,default="None")	
	response_header = models.CharField(max_length=200,default="None")	
	mod = models.BooleanField(default=False)
	def __str__(self):
		return self.host + " : " + self.map_name 
	def set_server_type(self,character):
		character = ord(character)
		if character == 100 or character == 68:
			self.server_type = "Dedicated"
		elif character == 108 or character == 76:
			self.server_type = "Non-Dedicated"
		elif character == 112 or character == 80:
			self.server_type = "SourceTV Relay"
		else:
			try:
				raise Exception("Unknown Server Type")
			except ValueError as err:
				self.server_type = "Dedicated"
				print err.args
	def set_environment(self,character):
		character = ord(character)
		if character == 119 or character == 87:
			self.environment = "Windows"
		elif character == 108 or character == 76:
			self.environment = "Linux"
		elif character == 109 or character == 77 or character == 111 or character == 79:
			self.environment = "Mac"
		else:
			try:
				raise Exception("Unknown Environment")
			except ValueError as err:
				self.environment = "Windows"
				print err.args
	def set_password_protected(self,num):
		if num == 0:
			self.password_protected = "No"
		elif num == 1:
			self.password_protected = "Yes"
		else:
			try:
				raise Exception("Unknown Visibility")
			except ValueError as err:
				self.password_protected = False
				print err.args
	def set_vac_secured(self,num):
		if num == 0:
			self.vac_secured = False
		elif num == 1:
			self.vac_secured = True
		elif num == None:
			self.vac_secured = False
		else:
			try:
				raise Exception("Unknown VAC")
			except ValueError as err:
				self.vac_secured = False
				print err.args
	def set_header_response(self,character):
		character = ord(character)
		if character == 109:
			self.response_header = "OLD"
		elif character == 73:
			self.response_header = "NEW"
		else:
			try:
				raise Exception("Unknown Header Response")
			except ValueError as err:
				self.response_header = "NEW"
				print err.args
	def dumps(self):
		return {"ip": self.ip,
				"map_name":self.map_name,
				"server_name":self.server_name,
				"num_players":self.num_players,
				"max_players":self.max_players,
				"num_bots":self.num_bots,
				"password_protected":self.password_protected
		}

class PlayerTemp(models.Model):
	server = models.ForeignKey(Server,null=True, blank=True)
	score = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name
	def dumps(self):
		return {
			"name":self.name,
			"score":self.score,
			"duration":self.duration,
		}