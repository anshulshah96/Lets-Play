from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LPapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^serverlist/', include('serverlist.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
)
