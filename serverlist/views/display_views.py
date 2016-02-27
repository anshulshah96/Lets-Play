from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
import logging
from serverlist.models import *
from django.views.decorators.cache import cache_page

@cache_page(20)
def index(request):
	latest_server_list = Server.objects.all()
	logging.debug(latest_server_list)
	for server in latest_server_list:
		server.link = server.ip.replace(".","_")
	context = {'latest_server_list': latest_server_list}
	return render(request,'serverlist/index.html',context)

def home(request):
	return redirect("/serverlist/")

@cache_page(20)
def ip_details(request,server_id):
	server_id = server_id.replace("_",".")
	server = get_object_or_404(Server, ip = server_id)
	player_list = PlayerTemp.objects.filter(server=server).order_by("-score")
	logging.debug(player_list)
	context = {'player_list': player_list,'server':server}
	return render(request,'serverlist/playerlist.html',context)

@cache_page(20)
def leader_board(request):
	leader_list = Player.objects.all().order_by("-score")[0:5]
	context = {'leader_list': leader_list}
	return render(request,'serverlist/leaderboard.html',context)