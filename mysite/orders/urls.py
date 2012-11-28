from django.conf.urls.defaults import *

urlpatterns = patterns('orders.views',
                       url(r'^new/$', 'new'),
                       )


from mysite.settings import ROOT

urlpatterns += patterns('',
                       (r'^static/(?P<path>.*)$',
                        'django.views.static.serve',
                        {'document_root': ROOT('person/static/')})
                       )
