from django.contrib import admin
from .models import Office, Candidate, Vote, Ballot


admin.site.register(Office)
admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register(Ballot)
