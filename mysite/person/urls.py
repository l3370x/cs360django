from django.conf.urls.defaults import *

urlpatterns = patterns('person.views',
                       url(r'^person/$', 'index'),
                       url(r'^person/(?P<id>\d+)/$', 'person'),
                       url(r'^dog/add/$', 'submit_dog'),
                       url(r'^dog/all/$', 'all'),
                       url(r'^dog/(?P<id>\d+)/$', 'dog'),
                       url(r'^dog/edit/(?P<id>\d+)/$', 'edit'),
                       url(r'^dog/delete/(?P<id>\d+)/$', 'delete'),
                       url(r'^dog/find/$', 'find'),
                       url(r'^auth/login/$', 'login'),
                       url(r'^auth/logout/$', 'logout'),
                       url(r'^auth/create/$', 'create'),
                       url(r'^$', 'home'),
                       )


from mysite.settings import ROOT

urlpatterns += patterns('',
                       (r'^static/(?P<path>.*)$',
                        'django.views.static.serve',
                        {'document_root': ROOT('person/static/')})
                       )
