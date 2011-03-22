from django.conf.urls.defaults import *
from settings import MEDIA_ROOT, MODULE
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                              { 'document_root' : MEDIA_ROOT }),
    (r'^$', MODULE + '.views.index'),
)

urlpatterns += patterns(MODULE + '.candidates.views',
    (r'^candidates/$', 'index'),
    (r'^candidates/(?P<username>[a-zA-Z0-9]+)/$', 'get_candidate'),
    (r'^candidates/(?P<username>[a-zA-Z0-9]+)/add/$', 'add_candidate'),
    (r'^candidates/(?P<username>[a-zA-Z0-9]+)/edit/$', 'edit_candidate'),
    (r'^candidates/(?P<username>[a-zA-Z0-9]+)/remove/$', 'remove_candidate'),
    
    (r'^offices/$', 'office_index'),
    (r'^offices/add/$', 'add_office'),
    (r'^offices/(?P<id>[0-9]+)/$', 'get_office'),
    (r'^offices/(?P<id>[0-9]+)/edit/$', 'edit_office'),
    (r'^offices/(?P<id>[0-9]+)/remove/$', 'remove_office'),
)

urlpatterns += patterns(MODULE + '.voting.views',
    (r'^voting/', 'index'),
    (r'^results/', 'results'),
)
    
# cas
urlpatterns += patterns('django_cas.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^logout/\?next=(?P<next_page>.+)$', 'logout', name='logout-with-next'),
)

