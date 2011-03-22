from django.conf.urls.defaults import *


urlpatterns = patterns('election.candidate.views',
    url(r'^candidates/$', 'candidate_index', name='candidate-index'),
    url(r'^candidates/(?P<username>[a-zA-Z0-9]+)/$', 'get_candidate',
        name='candidate-view'),
    url(r'^candidates/(?P<username>[a-zA-Z0-9]+)/add/$', 'add_candidate',
        name='candidate-add'),
    url(r'^candidates/(?P<username>[a-zA-Z0-9]+)/edit/$', 'edit_candidate',
        name='candidate-edit'),
    url(r'^candidates/(?P<username>[a-zA-Z0-9]+)/remove/$',
        'remove_candidate', name='candidate-remove'),

    url(r'^offices/$', 'office_index', name='office-index'),
    url(r'^offices/add/$', 'add_office', name='office-add'),
    url(r'^offices/(?P<id>[0-9]+)/$', 'get_office', name='office-view'),
    url(r'^offices/(?P<id>[0-9]+)/edit/$', 'edit_office',
        name='office-edit'),
    url(r'^offices/(?P<id>[0-9]+)/remove/$', 'remove_office',
        name='office-remove'),

    url(r'^$', 'index', name='index'),
)
urlpatterns += patterns('election.candidate.vote_views',
    url(r'^voting/$', 'index', name='vote-index'),
    url(r'^results/$', 'results', name='vote-results'),
)
urlpatterns += patterns('election.candidate.json_views',
    url(r'^offices/(?P<id>[0-9]+)/json/$', 'office_get',
        name='json-office-get'),
)
