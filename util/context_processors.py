from .candidates.models import Candidate

# A custom context processor which takes in a request and retrieves common
# items from the request used in many templates
def acm_election(request):
    try:
        candidate = Candidate.objects.get(username=request.user.username)
        has_candidate = True
    except:
        candidate = None
        has_candidate = False
    
    ## try and get any session messages
    try:
        # if we have messages, grab them and reset
        messages = request.session['messages']
        del request.session['messages']
    except KeyError:
        messages = []
    return {'messages'      : messages,
            #'candidate'     : candidate,
            'has_candidate' : has_candidate,}

