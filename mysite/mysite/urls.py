from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^person/', include('person.urls')),
    url(r'^orders/', include('orders.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', 'mysite.views.about'),
    url(r'^', include('person.urls')),
)

from mysite.settings import ROOT

urlpatterns += patterns('',
                       (r'^templates/static/(?P<path>.*)$',
                        'django.views.static.serve',
                        {'document_root': ROOT('templates/static/')})
                       )
