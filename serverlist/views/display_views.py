from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
import logging
from serverlist.models import *
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from itertools import chain

# def testm(request):
# 	latest_server_list = Server.objects.all()
# 	logging.debug(latest_server_list)
# 	for server in latest_server_list:
# 		server.link = server.ip.replace(".","_")
# 	leader_list_score = Player.objects.all().order_by("-score")[0:5]
# 	leader_list_duration = Player.objects.all().order_by("-duration")[0:5]
# 	context = {'latest_server_list': latest_server_list , 'leader_list_score': leader_list_score, 
# 				'leader_list_duration': leader_list_duration}
# 	return render(request,'serverlist/index2.html',context)

# def testp(request,server_id):
# 	server_id = server_id.replace("_",".")
# 	server = get_object_or_404(Server, ip = server_id)
# 	player_list = PlayerTemp.objects.filter(server=server).order_by("bot").order_by("-score")
# 	logging.debug(player_list)
# 	context = {'player_list': player_list,'server':server}
# 	return render(request,'serverlist/playerlist2.html',context)

# @cache_page(20)
def index(request):
	latest_server_list = Server.objects.all()
	logging.debug(latest_server_list)
	for server in latest_server_list:
		server.link = server.ip.replace(".","_")
	leader_list_score = Player.objects.all().order_by("-score")[0:5]
	leader_list_duration = Player.objects.all().order_by("-duration")[0:5]
	context = {'latest_server_list': latest_server_list , 'leader_list_score': leader_list_score, 
				'leader_list_duration': leader_list_duration}
	return render(request,'serverlist/index.html',context)

@cache_page(20)
def home(request):
	return redirect("/serverlist/")

# @cache_page(20)
def ip_details(request,server_id):
	server_id = server_id.replace("_",".")
	server = get_object_or_404(Server, ip = server_id)
	human_list = PlayerTemp.objects.filter(server=server,bot=False).order_by("-score")
	bot_list = PlayerTemp.objects.filter(server=server,bot=True).order_by("-score")
	player_list = list(chain(human_list,bot_list))
	logging.debug(player_list)
	context = {'player_list': player_list,'server':server}
	return render(request,'serverlist/playerlist.html',context)

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

def index2(request):
	latest_server_list = Server.objects.all()
	logging.debug(latest_server_list)
	for server in latest_server_list:
		server.link = server.ip.replace(".","_")
	leader_list_score = Player.objects.all().order_by("-score")[0:5]
	leader_list_duration = Player.objects.all().order_by("-duration")[0:5]
	context = {'latest_server_list': latest_server_list , 'leader_list_score': leader_list_score, 
				'leader_list_duration': leader_list_duration}
	return render(request,'serverlist2/index2.html',context)

def ip_details2(request,server_id):
	server_id = server_id.replace("_",".")
	server = get_object_or_404(Server, ip = server_id)
	human_list = PlayerTemp.objects.filter(server=server,bot=False).order_by("-score")
	bot_list = PlayerTemp.objects.filter(server=server,bot=True).order_by("-score")
	player_list = list(chain(human_list,bot_list))
	logging.debug(player_list)
	context = {'player_list': player_list,'server':server}
	return render(request,'serverlist2/playerlist2.html',context)