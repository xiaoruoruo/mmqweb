# encoding: utf8
import json
import re
import datetime
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseBadRequest
from django.db import transaction
from django.views.decorators.csrf import csrf_protect
from django.views.static import serve
from django.contrib.auth.decorators import permission_required

from club.models import Member, Activity


@csrf_protect
def csrf_serve(*args, **kwargs):
    """
    This is a hack: because django.middleware.csrf.process_response need this.
    """
    args[0].META['CSRF_COOKIE_USED'] = True
    return serve(*args, **kwargs)

class AngularJsCsrfMiddleware(object):
    """
    AngularJs's http service will set header X-XSRF-TOKEN.
    However Django will look for X-CSRFToken header.
    This middleware is used to replace the header to the desired name.
    """

    def process_request(self, request):
        ANGULAR_HEADER = 'HTTP_X_XSRF_TOKEN'
        DJANGO_HEADER = 'HTTP_X_CSRFTOKEN'
        if ANGULAR_HEADER in request.META:
            request.META[DJANGO_HEADER] = request.META[ANGULAR_HEADER]
            del request.META[ANGULAR_HEADER]
        return None

def index(request):
    return render_to_response('club-index.html',
            {},
            RequestContext(request))

@permission_required('club.add_activity', raise_exception=True)
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

    return HttpResponse("ok", mimetype="application/json")

@permission_required('club.add_member', raise_exception=True)
@transaction.commit_on_success
def new_member(request):
    if request.method == 'POST':
        l = json.loads( request.raw_post_data )
        print l
        member = Member(name = l['name'], male = l['male'])
        member.save()
    return HttpResponse("ok", mimetype="application/json")

def balance_sheet(request):
    "按照拼音排序，所有人的余额"
    members = Member.objects.all()
    members = list(members)
    members.sort(key=lambda m: m.index)
    return render_to_response('balance-sheet.html',
            {
                'members':members,
                'balance_sheet_active': True,
            },
            RequestContext(request))

def activity_sheet(request, name):
    "按照日期倒序，该会员的活动记录"
    member = get_object_or_404(Member, name=name)
    acts = Activity.objects.filter(member=member).order_by('-date', '-id')

    # calculate running totals
    acts = list(acts)
    acts.reverse()
    sum = 0.0
    running = []
    for a in acts:
        if a.deposit:
            sum += a.deposit
        if a.cost:
            sum -= a.cost
        running.append(sum)
    acts.reverse()
    running.reverse()

    return render_to_response('activity-sheet.html',
            {
                'activity-active': True,
                'activities':zip(acts, running),
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

