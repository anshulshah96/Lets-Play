from django.apps import AppConfig
import socket, sys
from struct import *
from serverlist.lib import *
from serverlist.maplib import *
import threading
import thread
import time
from serverlist.models import *
import logging
 
UDP_PORT = 27015
axlimits = [1,255]
aylimits = [1,255]
nslist = []
tplist = []
SLEEP_TIME = 10

class MyAppConfig(AppConfig):
	logging.basicConfig(level=logging.ERROR)
	name = 'serverlist'
	verbose_name = "My Application"
	def ready(self):
		def continuous_scan():
			global nslist
			global tplist
			global axlimits
			global aylimits
			while True:
				nslist = []
				tplist = []
				try:
				    scanner = SourceScanner(timeout = 5.0, axlimits = axlimits, aylimits = aylimits)
				    scanner.scanServers()
				    server_list = scanner.getServerList()
				    for info_elements in server_list:
						new_server = Server(ip = info_elements['host_ip'],map_name = info_elements['map'],host = info_elements['host_ip'],
										num_players = info_elements['numplayers'],max_players = info_elements['maxplayers'],
										server_name = info_elements['name'],game_name = info_elements['game'],folder = info_elements['folder'])
						new_server.set_server_type(info_elements['server_type'])
						new_server.set_environment(info_elements['environment'])
						new_server.set_password_protected(info_elements['password'])
						# new_server.set_vac_secured(info_elements['vac'])
						new_server.set_header_response(info_elements['header'])
						nslist.append(new_server)
						server = SourceQuery(info_elements['host_ip'],UDP_PORT)
						player_list = server.player()
						for player in player_list:
						    new_player = PlayerTemp(score = player['score'], name = player['name'], duration = player['duration'])
						    new_player.server_name = new_server.ip
						    tplist.append(new_player)
						info = info_elements['host_ip'] + " " + info_elements['header'] + " found: " + info_elements['map']
						logging.debug(info)
				    Server.objects.all().delete()
				    PlayerTemp.objects.all().delete()
				    for serv in nslist:
						serv.save()
						for player in tplist:
							if player.server_name == serv.ip:
								player.server = serv
								player.save()
				except KeyboardInterrupt:
					logging.info(str(len(nslist)) + " servers found exiting...")
					sys.exit(0)
					raise
				except Exception, msg:
					logging.exception(str(msg))
				logging.info(str(len(nslist)) + " servers found, sleeping for " + str(SLEEP_TIME) + " seconds")
				time.sleep(SLEEP_TIME)
		try:
			thread.start_new_thread(continuous_scan,())
		except Exception, e:
			logging.exception(str(e))
			sys.exit(0)

