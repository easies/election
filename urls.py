from django.conf.urls.defaults import *
from candidates.models import Candidate
from acm_election.settings import MEDIA_ROOT
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^election/acm_election/', include('acm_election.foo.urls')),

    # Uncomment this for admin:
    (r'^election/admin/(.*)', admin.site.root),
    #(r'^election/admin/',    include('django.contrib.admin.urls')),
    (r'^election/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^election/$',         'acm_election.views.index'),
    
    (r'^election/candidates/$','acm_election.candidates.views.index'),
    (r'^election/candidates/(?P<username>[a-zA-Z0-9]+)/$', 'acm_election.candidates.views.get_candidate'),
    (r'^election/candidates/(?P<username>[a-zA-Z0-9]+)/add/$', 'acm_election.candidates.views.add_candidate'),
    (r'^election/candidates/(?P<username>[a-zA-Z0-9]+)/edit/$', 'acm_election.candidates.views.edit_candidate'),
    (r'^election/candidates/(?P<username>[a-zA-Z0-9]+)/remove/$', 'acm_election.candidates.views.remove_candidate'),
    
    (r'^election/offices/$', 'acm_election.candidates.views.office_index'),
    (r'^election/offices/add/$', 'acm_election.candidates.views.add_office'),
    (r'^election/offices/(?P<id>[0-9]+)/$', 'acm_election.candidates.views.get_office'),
    (r'^election/offices/(?P<id>[0-9]+)/edit/$', 'acm_election.candidates.views.edit_office'),
    (r'^election/offices/(?P<id>[0-9]+)/remove/$', 'acm_election.candidates.views.remove_office'),
    
    (r'^election/voting/', 'acm_election.voting.views.index'),
    (r'^election/results/', 'acm_election.voting.views.results'),
)
    
# cas
urlpatterns += patterns('django_cas.views',
    url(r'^election/login/$', 'login', name="login"),
    url(r'^election/logout/$', 'logout', name="logout"),
    url(r'^election/logout/\?next=(?P<next_page>.+)$', 'logout', name="logout-with-next"),
)
