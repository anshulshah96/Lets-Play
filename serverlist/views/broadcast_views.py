from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
import json
from serverlist.models import *

def serverlist_json(request):
	latest_server_list = Server.objects.all()
	json_object = json.dumps([server.dumps() for server in latest_server_list])
	return HttpResponse(json_object)

def ip_details_json(request,server_id):
	server_id = server_id.replace("_",".")
	try:
		server = Server.objects.get(ip = server_id)
	except Server.DoesNotExist:
		raise Http404("Server Does Not Exist")
	player_list = PlayerTemp.objects.filter(server=server).order_by("-score")
	if len(player_list) == 0:
		return HttpResponse("No player is present")
	json_object = json.dumps([player.dumps() for player in player_list])
	return HttpResponse(json_object)