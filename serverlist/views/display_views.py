from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader

from serverlist.models import *


def index(request):
	latest_server_list = Server.objects.all()
	print latest_server_list
	for server in latest_server_list:
		server.link = server.ip.replace(".","_")
	context = {'latest_server_list': latest_server_list}
	return render(request,'serverlist/index.html',context)

def home(request):
	return redirect("/serverlist/")
	# return HttpResponse("You're at the home page.")

def ip_details(request,server_id):
	server_id = server_id.replace("_",".")
	server = get_object_or_404(Server, ip = server_id)
	player_list = PlayerTemp.objects.filter(server=server).order_by("-score")
	print player_list
	context = {'player_list': player_list,'server':server}
	return render(request,'serverlist/playerlist.html',context)
