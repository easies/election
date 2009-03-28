from acm_election.util import decorator
from acm_election.voting.models import Ballot
from exceptions import Exception
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

class SingleSignOnMismatch(Exception):
    def __init__(self):
        self.name = 'SingleSignOnMismatch'

class UserNotAuthenticated(Exception):
    def __init__(self):
        self.name = 'UserNotAuthenticated'
        
class UserHasVoted(Exception):
    def __init__(self):
        self.name = 'UserHasVoted'

class MissingVoteAdmin(Exception):
    def __init__(self):
        self.name = 'MissingVoteAdmin'

class VoteNotActive(Exception):
    def __init__(self):
        self.name = 'VoteNotActive'

class NotACMMember(Exception):
    def __init__(self):
        self.name = 'NotACMMember'

def election_routing(REDIRECT_TO='/',REVERSE=False):
    """ Catches exceptions and routes views. """
    
    mesgs = {'SingleSignOnMismatch' :
             """You are not logged in as the correct user. Please log in as the
                correct user and try again.""",
             'UserNotAuthenticated' :
             """You are not authenticated. Please log in any try again.""",
             'MissingVoteAdmin' :
             """You do not have the proper privlages to access the requested page.
                Please log in as user with correct privlages and try again.""",
             'UserHasVoted' :
             """You have already submitted a ballot for the vote. If this is a 
                mistake, please contact an ACM officer immediately.""",
             'VoteNotActive' :
             """Voting is not active. Please try again at a different time.""",
             'NotACMMember' :
             """You are not registered as an ACM member. If you feel this is a 
                mistake, contact an ACM officer immediately."""}
    
    @decorator
    def actual(f, request, *a, **kw):
        if REVERSE:
            redirect = reverse(REDIRECT_TO)
        else:
            redirect = REDIRECT_TO
        r = HttpResponseRedirect(redirect)
        try:
            return f(request,*a,**kw)
        except SingleSignOnMismatch, e:
            request.session['messages'] = [mesgs[e.name]]
            return r
        except UserNotAuthenticated, e:
            request.session['messages'] = [mesgs[e.name]]
            return r
        except MissingVoteAdmin, e:
            request.session['messages'] = [mesgs[e.name]]
            return r
        except UserHasVoted, e:
            request.session['messages'] = [mesgs[e.name]]
            return r
        except VoteNotActive, e:
            request.session['messages'] = [mesgs[e.name]]
            return r
        except NotACMMember, e:
            request.session['messages'] = [mesgs[e.name]]
            return r
    return actual

## authentication decorators
@decorator
def isSingleSignOn(f, request, username, *a, **kw):
    """
        This decorator requires both the user to be logged in, and the passed in
        username to match the logged in user's username.
    """
    ## Check to see if a user is logged in, and is the same user as username
    if not request.user.is_authenticated():
        raise UserNotAuthenticated()
    if request.user.username != username:
        try:
            request.user.groups.get(name='vote_admin')
        except:
            raise SingleSignOnMismatch()
    return f(request, username, *a,**kw)

@decorator
def isVoteAdmin(f, request, *a, **kw):
    """"
        This decorator requires both the user to be logged in, and the user to 
        belong to the vote_admin permission group.
    """
    # Check to see if the user is logged in
    if request.user.is_authenticated():
        try:
            request.user.groups.get(name='vote_admin')
        except Exception:
            raise MissingVoteAdmin()
    else:
        # if noone is logged in, or there is a mismatch error
        raise UserNotAuthenticated()
    return f(request, *a, **kw)

@decorator
def canVote(f, request, *a, **kw):
    """
        This decorator requires the user to be both logged in,
        and an acm member
    """
    ## If it is not vote time, tell them no
    from datetime import datetime
    b   = datetime(2009, 3, 30, 19, 0, 0, 0)
    e   = datetime(2009, 4, 3,  19, 0, 0, 0)
    n   = datetime.now()
    if not (b < n < e):
         raise VoteNotActive()
    # Check to see if the user is logged in
    if request.user.is_authenticated():
        ## If they are logged in, make sure they are in acm
        if request.user.username in [x.strip() for x in open(settings.ROOT('memberlist'))]:
            ## If they are in acm, make sure there is no ballot in their name
            try:
                Ballot.objects.get(voter=request.user.username)
            except:
                return f(request, *a, **kw)
            raise UserHasVoted()
        else:
	    raise NotACMMember()
    raise UserNotAuthenticated() 
