from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from serverlist.models import Server


def index(request):
	latest_server_list = Server.objects.all()
	print latest_server_list
	context = {'latest_server_list': latest_server_list}
	return render(request,'serverlist/index.html',context)
