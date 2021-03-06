# encoding: utf8
import datetime
import itertools
import json
import logging
import re
import urllib2, threading

from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_protect
from django.views.static import serve
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.views.decorators.cache import never_cache
from reversion import revisions as reversion
from htmlmin.decorators import not_minified_response

from club.models import Member, Activity

logger = logging.getLogger(__name__)

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
    return render(request, 'club-index.html')

def checkin(request):
    if request.method == 'GET':
        return checkin_GET(request)
    elif request.method == 'POST':
        return checkin_POST(request)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@permission_required('club.add_activity')
def checkin_GET(request):
    return render(request, 'checkin.html', {'checkin_active': True})

def send_log(tag, data):
    content = tag + " " + data
    if settings.DEBUG:
        print "send_log: %s" % content
        return
    if settings.LOG_API:
        urllib2.urlopen(settings.LOG_API, content).read()

@permission_required('club.add_activity', raise_exception=True)
def checkin_POST(request):
    threading.Thread(target=send_log, args=('checkin', request.body)).start()

    data = json.loads( request.body )
    # print data

    date = parse_date(data['date'])

    l = data['list']
    ver = data.get('ver', '1')
    if ver == '1':
        logger.error('checkin ver 1 is used')

    with reversion.create_revision():
        for o in l:
            # print o
            deposit = o['deposit']
            member = get_object_or_404(Member, name=o['name'], hidden=False)
            cost = determine_cost(member, o['weight'], ver)

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

    return HttpResponse("ok", content_type="application/json")

@permission_required('club.add_member', raise_exception=True)
def new_member(request):
    if request.method == 'POST':
        threading.Thread(target=send_log, args=('new_member', request.body)).start()
        l = json.loads( request.body )
        # print l
        member = Member(name = l['name'], male = l['male'])
        member.save()
        res = {'ok': {
            'name': member.name,
            'male': member.male,
            'index': member.index,
            'weight': -1
            }}
    return HttpResponse(json.dumps(res), content_type="application/json")

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
    return render(request, 'balance-sheet.html',
            {
                'members':members,
                'range': {'start': str(activity_start), 'end': str(activity_end)},
                'balance_sheet_active': True,
            })

def activity_sheet(request, name):
    "按照日期倒序，该会员的活动记录"
    member = get_object_or_404(Member, name=name, hidden=False)

    acts, running, sum = member.running_total()
    acts.reverse()
    running.reverse()

    return render(request, 'activity-sheet.html',
            {
                'activity-active': True,
                'activities':zip(acts, running),
                'member': member,
            })

@permission_required('club.add_activity', raise_exception=True)
@not_minified_response
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

    return render(request, 'activity-overall.html',
            {
                'activity_overall_active': True,
                'overall': overall
            })

@permission_required('club.add_activity', raise_exception=True)
def activity_by_date(request, act_date):
    d = parse_date(act_date)
    if not d:
        return HttpResponseBadRequest('')

    if request.method == 'GET':
        return activity_by_date_GET(d)
    elif request.method == 'POST':
        return activity_by_date_POST(request, d)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@never_cache
def activity_by_date_GET(d):
    "API: 返回某日的所有Activity"
    acts = list(Activity.objects.filter(date=d).select_related('member'))
    def to_json(a):
        return {
            'name': a.member.name,
            'cost': a.cost,
            'deposit': a.deposit,
        }
    acts = [to_json(a) for a in acts]
    return JsonResponse({
        'date': datetime.datetime.strftime(d, "%Y-%m-%d"),
        'activities': acts,
    })

@transaction.atomic
def activity_by_date_POST(request, d):
    "API: 修改某日的所有Activity"
    threading.Thread(target=send_log, args=('activity_by_date/%s' % d, request.body)).start()
    data = json.loads(request.body)

    with reversion.create_revision():
        # 1. Delete
        Activity.objects.filter(date=d).delete()

        # 2. Re-add
        acts = {}
        for a in data['activities']:
            name = a['name']
            mid = Member.objects.get(name=name, hidden=False).id
            a['member_id'] = mid
            if mid in acts:
                # Merge activities when member is duplicated.
                act = acts[mid]
                if 'weight' in a and a['weight']:
                    act['weight'] += a['weight']
                if 'deposit' in a and a['deposit']:
                    act['deposit'] += a['deposit']
            else:
                if 'weight' not in a or not a['weight']:
                    a['weight'] = 0
                if 'deposit' not in a or not a['deposit']:
                    a['deposit'] = 0
                acts[mid] = a
        for act in acts.values():
            a = Activity(member_id=act['member_id'], cost=act['weight'], deposit=act['deposit'], date=d)
            if a.cost or a.deposit:
                # Don't save when both cost and deposit are 0, basically delete this activity.
                a.save()

        # 3. Re-balance
        member_ids = acts.keys()
        for member in Member.objects.filter(id__in=member_ids):
            _, running, sum = member.running_total()
            if sum != member.balance:
                member.balance = sum
                member.save()
        reversion.set_user(request.user)

    # 4. Done
    return HttpResponse("ok", content_type="application/json")

def determine_cost(member, weight, ver):
    if ver == '1':
        return weight * member.cost
    elif ver == '2':
        # Always set member cost to 1.
        # TODO: there used to have a member-based weight. Clean up code related to that.
        return weight * 1
    else:
        raise Exception("Unknown ver: " + ver)

re_date = re.compile(r'(\d\d\d\d)-(\d\d?)-(\d\d?)')
def parse_date(date_string):
    m = re_date.match(date_string)
    if not m:
        return None
    return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

