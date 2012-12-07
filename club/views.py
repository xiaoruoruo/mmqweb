import json
import re
import datetime
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseBadRequest
from django.db import transaction

from club.models import Member, Activity


@transaction.commit_on_success
def checkin(request):
    if request.method == 'POST':
        data = json.loads( request.raw_post_data )
        print data

        date = parse_date(data['date'])

        l = data['list']
        for o in l:
            print o
            deposit = o['deposit']
            member = get_object_or_404(Member, name=o['name'])
            cost = determine_cost(member, o['weight'])

            a = Activity(
                member = member,
                weight = o['weight'],
                date = date,
                cost = cost,
                deposit = deposit,
            )
            a.save()

            member.balance -= cost
            if deposit:
                member.balance += deposit
            member.save()

    return HttpResponse("'ok'")

def balance_sheet(request):
    members = Member.objects.all()
    return render_to_response('balance_sheet.html',
            {'members':members},
            RequestContext(request))

def activity_sheet(request, name):
    member = Member.objects.get(name=name)
    acts = Activity.objects.filter(member=member)
    return render_to_response('activity_sheet.html',
            {
                'activities':acts,
                'member': member,
            },
            RequestContext(request))

def determine_cost(member, weight):
    if member.male:
        return weight * 15.0
    else:
        return weight * 10.0

re_date = re.compile(r'(\d\d\d\d)-(\d\d?)-(\d\d?)')
def parse_date(date_string):
    m = re_date.match(date_string)
    if not m:
        return HttpResponseBadRequest("'wrong date'")
    return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

@transaction.commit_on_success
def new_member(request):
    if request.method == 'POST':
        l = json.loads( request.raw_post_data )
        print l
        member = Member(name = l['name'], male = l['male'])
        member.save()
    return HttpResponse("'ok'")
