from django.conf.urls.defaults import *

urlpatterns = patterns('items.views',
                       url(r'^item/$', 'index'),
                       url(r'^item/(?P<id>\d+)/$', 'item'),
                       )

