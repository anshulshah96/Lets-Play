from django.apps import AppConfig
import socket, sys, os
import logging
import threading
import thread
import time
from serverlist.scan_module import *

class MyAppConfig(AppConfig):
	logging.basicConfig(level=logging.INFO)
	name = 'serverlist'
	verbose_name = "My Application"
	def ready(self):
		try:
			thread.start_new_thread(scan_repeater.continuous_scan,())
			pass
		except Exception, e:
			logging.exception(str(e))
			sys.exit(0)

