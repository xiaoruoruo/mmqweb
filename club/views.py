import json
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.db import transaction

from club.models import Member, Activity

@transaction.commit_on_success
def checkin(request):
    if request.method == 'POST':
        l = json.loads( request.raw_post_data )
        print l
        for o in l:
            print o
            member = get_object_or_404(Member, name=o['name'])
            a = Activity(member = member, weight = o['weight'])
            a.save()
    return HttpResponse("'ok'")
