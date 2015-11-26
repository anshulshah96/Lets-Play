from django.db import models

class Player(models.Model):
	name = models.CharField(max_length=200)
	duration = models.IntegerField(default=0)
	score = models.IntegerField(default=0)
	def __str__(self):
		return self.name

class Server(models.Model):
	ip = models.CharField(max_length=200)
	map_name = models.CharField(max_length=200)
	server_name = models.CharField(max_length=200)
	host = models.CharField(max_length=200)
	num_players = models.IntegerField(default=0)
	max_players = models.IntegerField(default=0)
	folder = models.CharField(max_length=200)
	def __str__(self):
		return self.host + " : " + self.map_name 

class PlayerTemp(models.Model):
	score = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name


	
