from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from ..candidates.models import Candidate, Office, CandidateForm, OfficeForm
from ..util.decorators import isSingleSignOn, isVoteAdmin, election_routing, SingleSignOnMismatch
from ..util.ldapmeta import get_user_metadata

def index(request):
    return render_to_response('candidates/index.html',
                              {'offices_fall' : Office.objects.filter(semester=1),
                               'offices_spr'  : Office.objects.filter(semester=2),
                               'orphens'      : Candidate.objects.filter(offices__isnull=True)},
                              context_instance=RequestContext(request))

def get_candidate(request, username):
    try:
        c = Candidate.objects.get(username=username)
    except:
        request.session['messages'] = ["User %s does not exist." % username]
        return HttpResponseRedirect(reverse(index))
    return render_to_response('candidates/view.html',
                              {'candidate' : c},
                              context_instance=RequestContext(request))

@login_required
@election_routing('acm_election.candidates.views.index',True)
def add_candidate(request, username):
    if not(request.user.username == username or request.user.is_staff):
        raise SingleSignOnMismatch()

    if request.method == 'POST':
        c    = Candidate(username=username)
        form = CandidateForm(request.POST, request.FILES,instance=c)
        if form.is_valid():
            c = form.save()
            return HttpResponseRedirect(reverse(get_candidate,kwargs={'username':username}))
    else:
        try:
            c = Candidate.objects.get(username=username)
            request.session['messages'] = ["User %s already exists." % username]
            return HttpResponseRedirect(reverse(get_candidate,kwargs={'username':username}))
        except:
            data  = get_user_metadata(username)
            data.update({ 'username' : username })
#            form = CandidateForm(initial={'username':username})
            form = CandidateForm(data)
    return render_to_response('modelform.html',
                              {'form'       : form,
                               'username'   : username},
                              context_instance=RequestContext(request))

@election_routing('acm_election.candidates.views.index',True)
@isVoteAdmin
def remove_candidate(request,username):
    try:
        c = Candidate.objects.get(username=username)
    except:
        request.session['messages'] = ["User %s does not exist." % username]
        return HttpResponseRedirect(reverse(index))
    if 'confirm-delete' in request.GET:
        c.delete()
        request.session['messages'] = ["Profile for %s deleted." % username]
        return HttpResponseRedirect(reverse(index))
    else:
        message = """Are you sure that you want to delete the profile for %s?
                     <a href='%s'>Confirm</a>"""
        tup = (username, reverse(remove_candidate, kwargs={'username':username}) + '?confirm-delete')
        request.session['messages'] = [message % tup]
        return HttpResponseRedirect(reverse(get_candidate,kwargs={'username':username}))
 
@election_routing('acm_election.candidates.views.index',True)
@isSingleSignOn
def edit_candidate(request,username):
    try:
        c = Candidate.objects.get(username=username)
    except:
        request.session['messages'] = ["User %s does not exist. Please create profile first." % username]
        return HttpResponseRedirect(reverse(add_candidate,kwargs={'username':username}))
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=c)
        if form.is_valid():
            c = form.save()
            return HttpResponseRedirect(reverse(get_candidate,kwargs={'username':username}))
    else:
        form = CandidateForm(instance=c)
    return render_to_response('modelform.html',
                              {'form'       : form,
                               'username'   : username},
                              context_instance=RequestContext(request))


def get_office(request,id):
    try:
        o = Office.objects.get(pk=id)
    except:
        request.session['messages'] = ["Office %s does not exist." % id]
        return HttpResponseRedirect(reverse(index))
    return render_to_response('offices/view.html',
                              {'office'     : o},
                              context_instance=RequestContext(request))

@election_routing('acm_election.candidates.views.index',True)
@isVoteAdmin
def office_index(request):
    return render_to_response('offices/index.html',
                              {'offices' : Office.objects.all()},
                              context_instance=RequestContext(request))

@election_routing('acm_election.candidates.views.index',True)
@isVoteAdmin
def add_office(request):
    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            try:
                o = form.save()
            except:
                request.session['messages'] = ["""Office and Semester combination must be unique."""]
            else:
                request.session['messages'] = ['Office "%s" created.' % o.title]
                return HttpResponseRedirect(reverse(office_index))
    else:
        form = OfficeForm()        
    return render_to_response('modelform.html',
                              {'form'       : form},
                              context_instance=RequestContext(request))    

@election_routing('acm_election.candidates.views.index',True)
@isVoteAdmin
def remove_office(request,id):
    try:
        o = Office.objects.get(pk=id)
    except:
        request.session['messages'] = ["Office %s does not exist." % id]
        return HttpResponseRedirect(reverse(office_index))
    if 'confirm-delete' in request.GET:
        title = o.title; o.delete()
        request.session['messages'] = ["Office %s deleted." % title]
        return HttpResponseRedirect(reverse(office_index))
    else:
        message = """Are you sure that you want to delete the office: %s?
                     <a href='%s'>Confirm</a>"""
        tup = (o.title, reverse(remove_office, kwargs={'id':id}) + '?confirm-delete')
        request.session['messages'] = [message % tup]
        return HttpResponseRedirect(reverse(office_index))

@election_routing('acm_election.candidates.views.index',True)
@isVoteAdmin
def edit_office(request,id):
    try:
        o = Office.objects.get(pk=id)
    except:
        request.session['messages'] = ["Office %s does not exist. Please create it first." % id]
        return HttpResponseRedirect(reverse(add_office))
    if request.method == 'POST':
        form = OfficeForm(request.POST, instance=o)
        if form.is_valid():
            try:
                o = form.save()
            except:
                request.session['messages'] = ["""Office and Semester combination must be unique."""]
            else:
                request.session['messages'] = ['Office "%s" saved.' % o.title]
                return HttpResponseRedirect(reverse(office_index))
    else:
        form = OfficeForm(instance=o)
    return render_to_response('modelform.html',
                              {'form'       : form},
                              context_instance=RequestContext(request))
