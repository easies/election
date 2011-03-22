from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^election/', include('urls')),
)

