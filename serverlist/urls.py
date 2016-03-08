from django.conf.urls import patterns, url

from serverlist import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^serverlist/$', views.index, name='index'),
    url(r'^serverlist/(?P<server_id>\w+)/$', views.ip_details, name='ip_details'),
 	url(r'^serverlist_json/$', views.serverlist_json, name='serverlist_json'),
    url(r'^serverlist_json/(?P<server_id>\w+)/$', views.ip_details_json, name='ip_details'),
 )