from django.apps import AppConfig
import socket, sys, os
import logging
import threading
import thread
import time
from serverlist.models import *
from serverlist.scan_module import *

class MyAppConfig(AppConfig):
	logging.basicConfig(level=logging.ERROR)
	name = 'serverlist'
	verbose_name = "My Application"
	def ready(self):

		# One Time Update LeaderBoard
		# leader_list = Player.objects.all()
		# for player in leader_list:
		# 	player.update_ratio()

		try:
			thread.start_new_thread(scan_repeater.continuous_scan,())
			pass
		except Exception, e:
			logging.exception(str(e))
			sys.exit(0)

