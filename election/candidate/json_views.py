from django.http import HttpResponse
from .models import Office


def office_get(request, id):
    try:
        o = Office.objects.get(pk=id)
    except Office.DoesNotExist:
        return HttpResponse('null', mimetype='application/json')
    # Dirty encode to JSON.
    desc = o.description.replace('\n', '\\n')
    desc = desc.replace('\r', '\\r')
    desc = desc.replace('\t', '\\t')
    json = '{"title":"%s","description":"%s"}' % (o.title, desc)
    return HttpResponse(json, mimetype='application/json')
