from django.conf.urls import url
from serverlist.views.display_views import *

from serverlist.views.broadcast_views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    # url(r'^serverlist/test/(?P<server_id>\w+)/$', testp, name='testp'),
    # url(r'^serverlist/test/$', testm, name='testm'),
    url(r'^serverlist/$', index, name='index'),
    url(r'^serverlist/(?P<server_id>\w+)/$', ip_details, name='ip_details'),
    url(r'^serverlist_json/$', serverlist_json, name='serverlist_json'),
    url(r'^serverlist_json/(?P<server_id>\w+)/$', ip_details_json, name='ip_details'),
]
