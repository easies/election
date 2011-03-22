import time
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from .models import Candidate, Office
from .forms import CandidateForm, OfficeForm
from .utils import get_user_metadata


def candidate_index(request):
    return render_to_response('candidate/candidate-index.html',
        {'offices_fall': Office.objects.filter(semester=1),
         'offices_spr': Office.objects.filter(semester=2),
         'orphans': Candidate.objects.filter(offices__isnull=True)},
        context_instance=RequestContext(request))


def get_candidate(request, username):
    try:
        u = User.objects.get(username=username)
        c = Candidate.objects.get(user=u)
    except (Candidate.DoesNotExist, User.DoesNotExist):
        messages.warning(request, 'User %s does not exist.' % username)
        return HttpResponseRedirect(reverse(index))
    return render_to_response('candidate/candidate-view.html',
        {'candidate' : c},
        context_instance=RequestContext(request))


@login_required
def add_candidate(request, username):
    user = request.user
    username_matches = user.username == username
    if not (username_matches or user.is_staff):
        raise SingleSignOnMismatch()
    if request.method == 'POST':
        if username_matches:
            c = Candidate(user=user)
        else:
            userinfo = get_user_metadata(username)
            if not userinfo:
                raise Exception('Unknown user')
            other, created = User.objects.get_or_create(username=username)
            other.email = userinfo['email']
            other.first_name = userinfo['first_name']
            other.last_name = userinfo['last_name']
            other.save()
            c = Candidate(user=other)
        form = CandidateForm(request.POST, request.FILES, instance=c)
        if form.is_valid():
            c = form.save()
            return HttpResponseRedirect(reverse(get_candidate,
                kwargs={'username': username}))
    else:
        form = CandidateForm()
        try:
            user = User.objects.get(username=username)
            if user.candidate:
                messages.warning(request, 'Candidate %s already exists.'
                    % username)
                return HttpResponseRedirect(reverse(get_candidate,
                    kwargs={'username': username}))
        except (Candidate.DoesNotExist, User.DoesNotExist):
            pass
    return render_to_response('candidate/model-form.html',
        {'form': form, 'username': username},
        context_instance=RequestContext(request))


@login_required
def remove_candidate(request, username):
    user = request.user
    if not (user.username == username or user.is_staff):
        return HttpResponseForbidden()
    try:
        u = User.objects.get(username=username)
        c = Candidate.objects.get(user=u)
    except (Candidate.DoesNotExist, User.DoesNotExist):
        messages.warning(request, 'User %s does not exist.' % username)
        return HttpResponseRedirect(reverse(index))
    if 'confirm-delete' in request.GET:
        c.delete()
        messages.warning(request, 'Profile for %s deleted.' % username)
        return HttpResponseRedirect(reverse(index))
    else:
        messages.warning(request, 'Are you sure that you want to delete '
            'the profile for %s <a href="%s?confirm-delete">Confirm</a>'
            % (username, reverse(remove_candidate,
                kwargs={'username': username})))
        return HttpResponseRedirect(reverse(get_candidate,
            kwargs={'username': username}))


@login_required
def edit_candidate(request, username):
    user = request.user
    if not (user.username == username or user.is_staff):
        return HttpResponseForbidden()
    try:
        c = Candidate.objects.get(user=user)
    except Candidate.DoesNotExist:
        message.warn(request, 'User %s does not exist. Please create '
            'profile first.' % username)
        return HttpResponseRedirect(reverse(add_candidate,
            kwargs={'username': username}))
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=c)
        if form.is_valid():
            c = form.save()
            return HttpResponseRedirect(reverse(get_candidate,
                kwargs={'username': username}))
    else:
        form = CandidateForm(instance=c)
    return render_to_response('candidate/model-form.html',
        {'form': form, 'username': username},
        context_instance=RequestContext(request))


def get_office(request, id):
    try:
        o = Office.objects.get(pk=id)
    except Office.DoesNotExist:
        raise Http404
    return render_to_response('candidate/office-view.html', {'office': o},
        context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def office_index(request):
    return render_to_response('candidate/office-index.html',
        {'offices' : Office.objects.all()},
        context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def add_office(request):
    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            try:
                o = form.save()
            except:
                messages.warning(request, 'Office and Semester combination '
                    'must be unique')
            else:
                messages.info(request, 'Office "%s" created.' % o.title)
                return HttpResponseRedirect(reverse(office_index))
    else:
        form = OfficeForm()
    return render_to_response('candidate/model-form.html', {'form': form},
        context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def remove_office(request, id):
    try:
        o = Office.objects.get(pk=id)
    except Office.DoesNotExist:
        messages.warning(request, 'Office %s does not exist.' % id)
        return HttpResponseRedirect(reverse(office_index))
    if 'confirm-delete' in request.GET:
        title = o.title
        o.delete()
        messages.info(request, 'Office %s deleted.' % title)
        return HttpResponseRedirect(reverse(office_index))
    else:
        messages.info(request, 'Are you sure that you want to delete '
            'the office: %s? <a href="%s?confirm-delete">Confirm</a>' %
            (o.title, reverse(remove_office, kwargs={'id': id})))
        return HttpResponseRedirect(reverse(office_index))


@user_passes_test(lambda u: u.is_staff)
def edit_office(request,id):
    try:
        o = Office.objects.get(pk=id)
    except Office.DoesNotExist:
        messages.warning(request, 'Office %s does not exist. '
            'Please create it first.' % id)
        return HttpResponseRedirect(reverse(add_office))
    if request.method == 'POST':
        form = OfficeForm(request.POST, instance=o)
        if form.is_valid():
            try:
                o = form.save()
            except:
                messages.warning(request, 'Office and semester combination '
                    'must be unique.')
            else:
                messages.info(request, 'Office "%s" saved.' % o.title)
                return HttpResponseRedirect(reverse(office_index))
    else:
        form = OfficeForm(instance=o)
    return render_to_response('candidate/model-form.html', {'form': form},
        context_instance=RequestContext(request))


def index(request):
    try:
        temp = request.session['server_mesg']
        del request.session['server_mesg']
    except:
        temp = []
    return render_to_response('candidate/index.html',
        {'election_year': time.strftime('%Y'),
         'election_open': True,
         'server_mesg': temp,
         'start_date': settings.VOTING_START,
         'end_date': settings.VOTING_END},
        context_instance=RequestContext(request))
