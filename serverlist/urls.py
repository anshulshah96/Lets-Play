from django.conf.urls import patterns, url

from serverlist import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)