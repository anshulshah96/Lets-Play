from django.apps import AppConfig
# from serverlist.celery import app
# from celery import Celery
import socket, sys
from struct import *
from serverlist.lib import *
import threading
import thread
import time
from serverlist.models import *

UDP_IP = "172.25.12.131"
UDP_PORT = 27015
exitFlag = 0
x_LOWER_LIMIT = 10
x_UPPER_LIMIT = 30
nslist = []

class MyAppConfig(AppConfig):
    name = 'serverlist'
    verbose_name = "My Application"
    def ready(self):
		thread.start_new_thread(continuous_scan,())
		pass

class myThread (threading.Thread):
    def __init__(self, hostaddress):
        threading.Thread.__init__(self)
        self.hostaddress = hostaddress
    def run(self):
        # print "Starting " + self.hostaddress
        scan(self.hostaddress)
        # print "Exiting " + self.hostaddress

def scan(hostaddress):
	global nslist
	try:
		server = SourceQuery(hostaddress, UDP_PORT)
		info_elements = server.info()
		new_server = Server(ip = hostaddress,map_name = info_elements['map'],host = info_elements['hostname'],num_players = info_elements['numplayers'],max_players = info_elements['maxplayers'])
		nslist.append(new_server)
		info = hostaddress+"  "+info_elements['header']+" found:  "+info_elements['map']
		print info
	except socket.error, msg:
		pass
def continuous_scan():
	global nslist
	while True:
		single_scan()
		print "The list is",nslist
		Server.objects.all().delete()
		for serv in nslist:
			serv.save()
		nslist = []
		print "List updated...sleeping for 10 sec"
		time.sleep(10)
	print "Exiting Main Thread"
def single_scan():
	tlist = []
	for x in range(x_LOWER_LIMIT,x_UPPER_LIMIT):
		print x
		for y in range(0,256):
			thread = myThread("172.25."+str(x)+"."+str(y))
			thread.start()
			tlist.append(thread)
		for t in tlist:
			t.join()
		tlist = []
	print "Scan Complete"
