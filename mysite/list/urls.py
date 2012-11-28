from django.conf.urls.defaults import *

urlpatterns = patterns('list.views',
                       url(r'^item/$', 'index'),
                       url(r'^item/(?P<id>\d+)/$', 'item'),
                        url(r'^item/add/$', 'add'),
                        url(r'^item/edit/(?P<id>\d+)/$', 'edit'),
                        url(r'^item/delete/(?P<id>\d+)/$', 'delete'),
                        url(r'^auth/login/$', 'login'),
                       url(r'^auth/logout/$', 'logout'),
                        url(r'^auth/create/$', 'create'),
                        url(r'^item/today/(?P<id>\d+)/$', 'today'),
                        url(r'^item/later/(?P<id>\d+)/$', 'later'),
                       )

from mysite.settings import ROOT

urlpatterns += patterns('',
                       (r'^static/(?P<path>.*)$',
                        'django.views.static.serve',
                        {'document_root': ROOT('list/static/')})
                       )
