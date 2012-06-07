# encoding:utf-8
import re

from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.template.loader import render_to_string

import parser
from game.models import Tournament, MatchGroup, Participation, Ranking, PersonalRating
from namebook.models import Entity

class TextForm(forms.Form):
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'rows':'10', 'cols':'80'}))
class MatchTextForm(forms.Form):
    source = forms.CharField(label="", widget=forms.Textarea(attrs={'rows':'15', 'cols':'80'}))


def index(request):
    t = Tournament.objects.order_by('id')
    if t.count()>0:
        t = t[0]
        return tournament_index(request, t.id, t)
    else:
        return render_to_response("game_index.html", {}, RequestContext(request))

def login_user(request):
    state = ""
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                return redirect('game.views.index')
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('login.html',{'state':state, 'username': username},
            RequestContext(request))

def tournament_index(request, tid, tournament=None):
    t = tournament
    if not t:
        t = get_object_or_404(Tournament, id=tid)
    groups = t.matchgroup_set.all()
    group_views = []
    for group in groups:
        view = find_match_group_view(group.view_name)
        try:
            v = view(group)
        except:
            raise
        # except e:
        #     v = unicode(e)
        group_views.append(v)
    return render_to_response("game_index.html",
                            {'tournament':t,
                            'group_views':group_views
                            }, RequestContext(request))

@permission_required('game.change_tournament')
def tournament_edit(request, tid, text_status="", addmatch_status="", match_text=""):
    t = Tournament.objects.get(id=tid)
    match_group_count = t.matchgroup_set.count()
    if match_group_count > 1:
        raise NotImplementedError("need template work")
    match_groups = t.matchgroup_set.all()
    form_text = TextForm(initial={'text':t.text})
    form_match = MatchTextForm(initial={'source':match_text})
    p_list = t.participants.all()
    return render_to_response("tedit.html",
                              {'tournament':t,
                               'match_groups' : match_groups,
                              'form_text':form_text, 'text_status':text_status,
                              'form_match':form_match, 'addmatch_status':addmatch_status,
                              'participation_list': p_list,
                              }, RequestContext(request))

def matches(request, mgid):
    mg = MatchGroup.objects.get(id=mgid)
    matches = sorted(mg.match_set.all(), reverse=True)
    return render_to_response("matches.html", {'mg':mg,'matches':matches}, RequestContext(request))

@permission_required('game.change_tournament')
def tournament_edit_text(request, tid):
    t = Tournament.objects.get(id=tid)
    status=u""
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            t.text=form.cleaned_data['text']
            t.save()
            status=u"修改成功！"
        else:
            status=u"修改失败？？"
    return tournament_edit(request, tid, text_status=status)

@permission_required('game.change_tournament')
def tournament_add_matches(request, tid):
    t = Tournament.objects.get(id=tid)
    status = u""
    if request.method == 'POST':
        form = MatchTextForm(request.POST)
        if form.is_valid():
            try:
                count = do_add_matches(t, form.cleaned_data['source'])
                status=u"添加成功%d条比赛记录！" % count
                return tournament_edit(request, tid, addmatch_status=status)
            except parser.ParseError as e:
                status=u"错误：%s" % (unicode(e),  )
                return tournament_edit(request, tid, addmatch_status=status, match_text=form.cleaned_data['source'])

@transaction.commit_on_success
def tournament_add_participation(request, tid=None):
    t = Tournament.objects.get(id=tid)
    status=u""
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            text=form.cleaned_data['text']
            count = 0
            for line in text.split('\n'):
                if not line: continue
                m = re.match(r"(?P<a>\w+)([,，、](?P<b>\w+))?(?P<g>\w+)?", line, re.UNICODE)
                if m:
                    a,b,g = m.group('a'), m.group('b'), m.group('g')
                    # TODO resolve entity instead of universally create one
                    pa = Entity(name=a)
                    pa.save()
                    if b:
                        pb = Entity(name=b)
                        pb.save()
                    p = Participation(tournament = t, playera = pa)
                    if b: p.playerb = pb
                    if g: p.represent = Entity.objects.filter(name__exact=g)
                    p.save()
                    count += 1
                else:
                    status = u"格式错误：%s" % line
            if not status:
                status=u"成功添加%d位(对)参赛人员！" % count
                form = TextForm()
        else:
            status=u"失败？？"
    else:
        form = TextForm()
    return render_to_response("add_participation.html", {'tournament':t, 'form': form, 'status': status})

@transaction.commit_on_success
def do_add_matches(tournament, source):
    mgs = list(tournament.matchgroup_set.all())
    if len(mgs) != 1:
        raise NotImplementedError()
    mg = mgs[0]
    count = 0
    for record in parse_blocks(source):
        mg.addMatch(record)
        count+=1
    return count

def parse_blocks(source):
    block = None
    for line in source.split('\n'):
        line=line.strip()
        if line=="":
            if block: yield block
            block = None
        else:
            if block:
                block += "\n" + line
            else:
                block = line
    if block: yield block

# MatchGroup views
def find_match_group_view(name):
    for v in match_group_views:
        if v.__name__ == name:
            return v
    return MG_default
def MG_default(mg):
    return render_to_string('MG_default.html', {
        'mg': mg
    })
def MG_naive(mg):
    ss = []
    ss.append(render_to_string('MG_default.html', {
        'mg': mg
    }))
    for ranking in mg.ranking_set.all():
        ss.append(ranking_render(ranking))
    return ''.join(ss)

def MG_roundrobin(mg):
    pass
match_group_views = [MG_default, MG_roundrobin, MG_naive]

# Ranking views
def ranking_index(request, ranking_id):
    r = get_object_or_404(Ranking, id=ranking_id)
    html = ranking_render(r)
    return render_to_response("ranking_index.html", {
        'ranking': r,
        'ranking_html': html,
        }, RequestContext(request))

def ranking_render(ranking):
    if ranking.type == 4 or ranking.type == 5:
        #ranker = ranking.get_ranker()
        #scores = ranker.print_by_type(Entity.Man) + ranker.print_by_type(Entity.Woman)
        #return render_to_string('ranking_simple.html', {
        #    'name': ranking.name,
        #    'scores': scores,
        #})
        return render_to_string('ranking_link.html', {
            'ranking': ranking,
            })

def ranking_person(request, ranking_id, name):
    "个人排名的积分变化过程显示，包括单双打"
    rs = get_list_or_404(PersonalRating, ranking__id=ranking_id, player__name=name)
    rs.reverse()
    return render_to_response("ranking_person.html", {
        'player': rs[0].player,
        'ranking': rs[0].ranking,
        'ratings': rs,
        }, RequestContext(request))
