from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime
from .models import Ballot
from .forms import VoteForm
from .decorators import is_member, has_not_voted, voting_open


@login_required
@is_member
@has_not_voted
@voting_open
def index(request):
    user = request.user
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            form.save(user, request.META['REMOTE_ADDR'])
            messages.info(request, 'Thank you for voting.')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = VoteForm()
        wris = [form[x] for x in form.fields if 'wri' in x]
        sels = [form[x] for x in form.fields if 'sel' in x]
        matches = [{'sel': x, 'wri': y} for x, y in zip(sels,wris)]
    return render_to_response('candidate/vote-form.html',
        {'pairs': matches},
        context_instance=RequestContext(request))


# XXX hide?
def results(request):
    if datetime.now() < settings.VOTING_END:
        messages.info(request, 'Results will be available when '
            'voting ends on %s' % str(settings.VOTING_END))
        return HttpResponseRedirect(reverse('index'))
    total_votes = Ballot.objects.count()
    from django.db import connection
    cursor = connection.cursor()
    query = """SELECT 
                 title, semester, cast_for, count(cast_for) as votes 
               FROM 
                 candidate_vote, candidate_office 
               WHERE 
                 candidate_vote.office_id = candidate_office.id 
               GROUP BY 
                 candidate_vote.office_id, cast_for 
               ORDER BY 
                 sort, semester;"""
    cursor.execute(query)
    results = cursor.fetchall()
    fall = []
    spring = []
    semesters = ('', 'Fall', 'Spring')
    for r in results:
        o, s, f, c = r
        data = {'office': o, 'candidate': f, 'total': c}
        if s == 1:
            fall.append(data)
        else:
            spring.append(data)
    return render_to_response('candidate/vote-results.html',
        {'spring': spring, 'fall': fall, 'total': total_votes},
        context_instance=RequestContext(request)) 
