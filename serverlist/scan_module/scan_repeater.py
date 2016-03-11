import socket, struct, sys
import logging
import time
import threading

from serverlist.models import *
from struct import *
from map_lib import *
from player_lib import *

UDP_PORT = 27015
axlimits = [1,35]
aylimits = [1,255]
nslist = []
tplist = []
old_player_list = []
SLEEP_TIME = 10

bot_suffix_list = []

def check_bot(name):
	for difficulty in bot_suffix_list:
		for bot_name in difficulty:
			if(name.endswith(bot_name)):
				return True;
	return False;

def update_leaderboard(player_obj):
	if player_obj.bot:
		return
	player_query = Player.objects.filter(name = player_obj.name)

	if len(player_query) == 0:
		new_player_regitered = Player(name = player_obj.name, duration = player_obj.duration, score = player_obj.score)
		new_player_regitered.update_ratio()
		logging.info("New player: " + new_player_regitered.name)
		new_player_regitered.save()
	else:
		player_update = player_query[0]
		player_update.score = player_update.score + player_obj.score
		player_update.duration = player_update.duration + player_obj.duration
		player_update.update_ratio()
		player_update.save()
		logging.info("LB update for: " + player_obj.name)
	return

def update_server_list(new_server_list):
	old_server_list = Server.objects.all()

	checklist = []
	for server_obj in new_server_list:
		if not 'map' in server_obj:
			logging.error("server_obj scanned has no map" + str(server_obj))
			continue
		new_dictionary = {
			'map_name' : server_obj['map'],
			'host' : server_obj['host_ip'],				'num_players' : server_obj['numplayers'],
			'max_players' : server_obj['maxplayers'], 	'server_name' : server_obj['name'],
			'game_name' : server_obj['game'],			'folder' : server_obj['folder'],
			'protocol' : server_obj['protocol'],		'num_bots' : server_obj['bots'],
			'num_humans' : server_obj['numplayers'] - server_obj['bots']
		}
		obj, created = Server.objects.update_or_create(ip = server_obj['host_ip'], defaults = new_dictionary)
		checklist.append(obj.ip)

		obj.set_server_type(server_obj['server_type'])
		obj.set_environment(server_obj['environment'])
		obj.set_password_protected(server_obj['password'])
		# obj.set_vac_secured(server_obj['vac'])
		obj.set_header_response(server_obj['header'])
		obj.save()

		if created:
			logging.debug("Created: " + obj.ip)
		else:
			logging.debug("Present: " + obj.ip)

	for server_obj in old_server_list:
		if not server_obj.ip in checklist:
			logging.debug("Deleting: " + server_obj.ip)
			server_obj.delete()

def update_player_list(new_player_list):
	old_player_list = PlayerTemp.objects.all()

	for player in old_player_list:
		logging.debug("OLD Found: " + player.name + ' in ' + player.server.ip)

	checklist = []

	for player_obj in new_player_list:
		new_dictionary = {
			'score' : player_obj['score'], 'duration' : int(player_obj['duration'])	, 'bot' : player_obj['bot']
		}
		obj, created = PlayerTemp.objects.update_or_create(server = player_obj['server_obj'], name = player_obj['name'], defaults = new_dictionary)
		
		checklist.append((obj.name,obj.server))

		if created:
			logging.debug("Created Player: " + obj.name)
		else:
			logging.debug("Present Player: " + obj.name)

	for player_obj in old_player_list:
		if not (player_obj.name,player_obj.server) in checklist:
			update_leaderboard(player_obj)
			player_obj.delete()

def continuous_scan():
			keys = open('serverlist/scan_module/bot_names.txt')
			for line in keys:
			        names = line.replace("\t"," ").strip().split(" ");
			        bot_suffix_list.append(names)
			keys.close()

			global nslist
			global tplist
			global axlimits
			global aylimits
			while True:
				nslist = []
				tplist = []
				try:
				    scanner = SourceScanner(timeout = 10.0, axlimits = axlimits, aylimits = aylimits)
				    scanner.scanServers()

				    new_server_list = scanner.getServerList()

				    nslist = Server.objects.all()
				    for serv in nslist:
				    	player_query = PlayerQuery(serv.ip,UDP_PORT)
				    	player_query.host = serv.ip
				    	player_list = player_query.player()
				    	for player in player_list:
						    player['server_obj'] = serv
						    if player['duration'] == -1:
						    	player['duration'] = 0
						    if player['score'] < 0:
						    	player['score'] = 0
						    player['duration'] /= 60 #duration is in minutes
						    player['bot'] = check_bot(player['name'])

						    tplist.append(player)
				    
				    update_player_list(tplist)
				    update_server_list(new_server_list)

				except KeyboardInterrupt:
					logging.info(str(len(nslist)) + " servers found exiting...")
					sys.exit(0)
					raise
				except Exception, msg:
					logging.exception(str(msg))
				logging.info(str(len(nslist)) + " servers found, sleeping for " + str(SLEEP_TIME) + " seconds")
				time.sleep(SLEEP_TIME)