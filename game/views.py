from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from models import *

def index(request):
    t = Tournament.objects.order_by('-id')[0]
    return render_to_response("index.html",{'tournament':t})
    
def tournament_edit(request, tid):
    t = Tournament.objects.get(id=tid)
    return render_to_response("tedit.html", {'tournament':t})

def tournament_matches(request, tid):
    t = Tournament.objects.get(id=tid)
    pass
