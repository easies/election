from django import forms
from .models import Candidate, Office, Ballot, Vote


class CandidateForm(forms.ModelForm):

    class Meta:
        model = Candidate
        exclude = ['user']


class OfficeForm(forms.ModelForm):

    class Meta:
        model = Office


class VoteForm(forms.Form):

    def add_office(self, office):
        NO_CONF = ('', '--No Confidence--')
        WRITE_IN = ('WRITE_IN', '--Use Write In--')
        # Build the candidate list.
        choices = [NO_CONF]
        for c in office.candidates.all():
            choices.append((c.username, c.full_name))
        choices.append(WRITE_IN)
        # Create the selectable field.
        sel = forms.ChoiceField(choices=choices)
        sel.label = office.full_title
        sel.required = False
        self.fields[office.full_title + "_sel"] = sel
        # Create the write in textbox.
        wri = forms.CharField(max_length=30)
        wri.label = office.full_title
        wri.required = False
        self.fields[office.full_title + "_wri"] = wri

    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        for office in Office.objects.all():
            self.add_office(office)

    def save(self, user, ip, commit=True):
         ballot = Ballot(voter=user, ip=ip)
         for office in Office.objects.all():
             sel = office.full_title + '_sel'
             wri = office.full_title + '_wri'
             if self.cleaned_data[sel] and self.cleaned_data[sel] is not '':
                 if self.cleaned_data[sel] == 'WRITE_IN':
                     vote_for = self.cleaned_data[wri]
                 else:
                     vote_for = self.cleaned_data[sel]
                 vote = Vote(office=Office.objects.get(pk=office.pk),
                    cast_for=vote_for)
                 vote.save()
         ballot.save()
         return True
