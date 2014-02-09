# encoding: utf8
import json
import re
import datetime
import itertools
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.db import transaction
from django.views.decorators.csrf import csrf_protect
from django.views.static import serve
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.core.exceptions import PermissionDenied
import reversion
import pyotp

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

def checkin(request):
    if request.method == 'GET':
        return checkin_GET(request)
    elif request.method == 'POST':
        return checkin_POST(request)
    else:
        raise HttpResponseNotAllowed(['GET', 'POST'])

@permission_required('club.add_activity')
def checkin_GET(request):
    return render_to_response('checkin.html',
            {'checkin_active': True},
            RequestContext(request))

@permission_required('club.add_activity', raise_exception=True)
def checkin_POST(request):
    data = json.loads( request.body )
    print data

    date = parse_date(data['date'])

    l = data['list']

    with reversion.create_revision():
        for o in l:
            print o
            deposit = o['deposit']
            member = get_object_or_404(Member, name=o['name'], hidden=False)
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
        reversion.set_user(request.user)
        reversion.set_comment('Checkin %d members' % len(l))

    return HttpResponse("ok", mimetype="application/json")

@permission_required('club.add_member', raise_exception=True)
def new_member(request):
    if request.method == 'POST':
        l = json.loads( request.body )
        print l
        member = Member(name = l['name'], male = l['male'])
        member.save()
        res = {'ok': {'name': member.name, 'index': member.index, 'weight': -1}}
    return HttpResponse(json.dumps(res), mimetype="application/json")

def balance_sheet(request):
    "Balance sheet during select date range, of all visible members, sorted by name index."
    filter_start = request.GET.get('start', None)
    filter_end = request.GET.get('end', None)

    members_dict = {}

    activity_start = datetime.date.today()
    activity_end = datetime.date(2000,1,1)

    activities = Activity.objects
    # string date filtering
    if filter_start:
        activities = activities.filter(date__gte=filter_start)
    if filter_end:
        activities = activities.filter(date__lte=filter_end)

    for a in activities.select_related('member'):
        if a.member.hidden:
            continue
        m = members_dict.get(a.member.id, None)
        if not m:
            m = a.member
            m.balance = 0
            members_dict[m.id] = m
        m.balance -= a.cost
        if a.deposit:
            m.balance += a.deposit

        if a.date < activity_start:
            activity_start = a.date
        if a.date > activity_end:
            activity_end = a.date

    members = members_dict.values()
    members.sort(key=lambda m: m.index)
    return render_to_response('balance-sheet.html',
            {
                'members':members,
                'range': {'start': str(activity_start), 'end': str(activity_end)},
                'balance_sheet_active': True,
            },
            RequestContext(request))

def activity_sheet(request, name):
    "按照日期倒序，该会员的活动记录"
    member = get_object_or_404(Member, name=name, hidden=False)

    acts, running, sum = member.running_total()
    acts.reverse()
    running.reverse()

    return render_to_response('activity-sheet.html',
            {
                'activity-active': True,
                'activities':zip(acts, running),
                'member': member,
            },
            RequestContext(request))

@permission_required('club.add_activity', raise_exception=True)
def activity_overall(request):
    "活动总表"
    overall = []

    all_acts = Activity.objects.order_by('-date').select_related('member')
    for date, acts in itertools.groupby(all_acts, lambda a: a.date):
        current_date = u"%s" % date
        current_activities = []
        for a in acts:
            current_activities.append({'member': a.member, 'cost': a.cost, 'deposit': a.deposit})
        overall.append({'date': current_date, 'acts': current_activities})

    return render_to_response('activity-overall.html',
            {
                'activity_overall_active': True,
                'overall': overall
            },
            RequestContext(request))


def dump_db(request):
    "Dump the db file for backup"
    totp = pyotp.TOTP(settings.OTP_SECRET)
    if request.GET.get('otp', None) == str(totp.now()):
        return serve(request, 'mmqweb.db', settings.SITE_ROOT)
    else:
        raise PermissionDenied()

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

