from django.db import models
from acm_election.candidates.models import Office
from django import forms
from django.conf import settings
from django.db.models.signals import pre_save, post_save, post_delete
from datetime import datetime

class Vote(models.Model):

    office              = models.ForeignKey(Office)
    office.verbose_name = "Office"

    cast_for = models.CharField(max_length=30)
    cast_for.verbose_name = "Vote Cast"

    def __unicode__(self):
        return str(self.office) + ' : ' + self.cast_for

def audit_model(sender, instance, **kwargs):
    if kwargs.has_key('deleted') and kwargs['deleted']:
        action = 'DELETE'
    elif ((kwargs.has_key('created') and kwargs['created']) or
          (instance.pk == None)):
        action = 'NEW'
    else:
        action = 'EDIT'

    audit_message = '%s %s %s %s\n' % (str(datetime.now()),
                                       str(instance.pk),
                                       action,
                                       str(instance))

    try:
        fp = open(settings.AUDIT_LOG, 'a+')
        fp.write(audit_message)
        close(fp)
    except:
        pass

def audit_model_delete(sender, instance, **kwargs):
    audit_model(sender, instance, created=False, deleted=True, **kwargs)
    
pre_save.connect(audit_model, sender=Vote)
post_save.connect(audit_model, sender=Vote)
post_delete.connect(audit_model_delete, sender=Vote)

class Ballot(models.Model):
    """ Represents a voting ballot. Used to keep track of who has voted. 
        No link to actual votes. """

    ## ---------- Attributes ------------------------------------------------##
    ## Username of person who has voted
    voter              = models.CharField(max_length=30)
    voter.verbose_name = "Voter (CCIS Username)"

    ## When this ballot was created. Good for tracking when a vote was made
    voted_at    = models.DateTimeField(auto_now_add=True)

    ## IPAddress of the person who voted. Tracking issue.
    ip          = models.IPAddressField()

    ## ---------- Methods ---------------------------------------------------##
    def __unicode__(self):
        return self.voter

class VoteForm(forms.Form):
    def __init__(self,*a, **kw):
        forms.Form.__init__(self,*a,**kw)
        NoConf = ('', '--No Confidence--')
        WritIn = ('WRITE_IN', '--Use Write In--')
        for office in Office.objects.all():
            choices = [NoConf]
            for cand in office.candidate_set.all():
                p = (cand.username, cand.fullname())
                choices.append(p)
            choices.append(WritIn)
            sel = forms.ChoiceField(choices=choices)
            sel.label = office.fulltitle()
            sel.required = False
            self.fields[office.fulltitle() + "_sel"] = sel
            wri = forms.CharField(max_length=30)
            wri.label = office.fulltitle()
            wri.required = False
            self.fields[office.fulltitle() + "_wri"] = wri
    
    def save(self, username, ip, commit=True):
         ballot = Ballot(voter=username,ip=ip)
         for office in Office.objects.all():
             sel = office.fulltitle()+"_sel"
             wri = office.fulltitle()+"_wri"
             if self.cleaned_data[sel] and self.cleaned_data[sel] is not '':
                 if self.cleaned_data[sel] == 'WRITE_IN':
                     vote_for = self.cleaned_data[wri]
                 else:
                     vote_for = self.cleaned_data[sel]
                 vote = Vote(office=Office.objects.get(pk=office.pk),cast_for=vote_for)
                 vote.save()
         ballot.save()
         return True

pre_save.connect(audit_model, sender=Ballot)
post_save.connect(audit_model, sender=Ballot)
post_delete.connect(audit_model_delete, sender=Ballot)
