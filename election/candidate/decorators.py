import functools
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from .utils import get_members
from .models import Ballot
from .views import index
from datetime import datetime


def is_member(f):
    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.user.username in get_members():
            return f(request, *args, **kwargs)
        messages.warning(request, 'You must be a member.')
        return HttpResponseRedirect(reverse(index))
    return wrapper


def has_not_voted(f):
    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        try:
            request.user.ballot
            messages.warning(request, 'You have already voted.')
        except Ballot.DoesNotExist:
            return f(request, *args, **kwargs)
        return HttpResponseRedirect(reverse(index))
    return wrapper


def voting_open(f):
    start = settings.VOTING_START
    end = settings.VOTING_END
    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        now = datetime.now()
        if start <= now <= end:
            return f(request, *args, **kwargs)
        messages.warning(request, 'Voting has been closed.')
        return HttpResponseRedirect(reverse(index))
    return wrapper
