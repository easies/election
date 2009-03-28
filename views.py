from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from candidates.models import Candidate, Office
import time

def index(request):
    try:
        temp = request.session['server_mesg']
        del request.session['server_mesg']
    except: temp = []
    return render_to_response('index.html',
                              {'election_year' : time.strftime('%Y'),
                               'election_open' : True,
                               'server_mesg'   : temp},
                               context_instance=RequestContext(request))