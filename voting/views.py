from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from acm_election.util.decorators import election_routing, canVote, isVoteAdmin
from acm_election.voting.models import VoteForm, Ballot
from acm_election.views import index as root_index

@election_routing('acm_election.views.index',True)
@canVote
def index(request):
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            form.save(request.user.username,request.META['REMOTE_ADDR'])
            request.session['messages'] = ["Thank you for voting."] 
            return HttpResponseRedirect(reverse(root_index))
    else:
        form = VoteForm()
        wris = [form[x] for x in form.fields if 'wri' in x]
        sels = [form[x] for x in form.fields if 'sel' in x]
        matches = [{'sel': x, 'wri': y} for x,y in zip(sels,wris)]
    return render_to_response('voteform.html',
                              {'pairs':matches},
                              context_instance=RequestContext(request))

@election_routing('acm_election.views.index', True)
@isVoteAdmin
def results(request):
    total_votes = Ballot.objects.count()
    from django.db import connection
    cursor = connection.cursor()
    query = """SELECT 
                 title, semester, cast_for, count(cast_for) as votes 
               FROM 
                 voting_vote, candidates_office 
               WHERE 
                 voting_vote.office_id = candidates_office.id 
               GROUP BY 
                 voting_vote.office_id, cast_for 
               ORDER BY 
                 sort, semester;"""
    cursor.execute(query)
    results = cursor.fetchall()
    fall = []; spring = []; semesters = ('','Fall','Spring')
    for r in results:
        o, s, f, c = r
        data = {'office':o, 'candidate':f, 'total':c}
        if s == 1:
            fall.append(data)
        else:
            spring.append(data)
    return render_to_response('voting/results.html',
                              {'spring':spring, 'fall':fall,'total':total_votes},
                              context_instance=RequestContext(request)) 
