from models import *

from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.db import transaction
from django.contrib.auth.decorators import permission_required

def index(request):
    return render_to_response("index.html")

def submit(request):
    if request.method != 'POST':
        raise Http404
    ip = request.META['HTTP_X_REAL_IP']
    json = request.POST.keys()[0]
    r = GameRecord(ip=ip, json=json)
    r.save()
    return HttpResponse(status=200)
