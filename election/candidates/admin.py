from django.contrib import admin
from models import Candidate, Office

#class CandidateAdmin(admin.ModelAdmin):
#    pass

admin.site.register(Candidate)
admin.site.register(Office)
#admin.site.register(Candidate, CandidateAdmin)
