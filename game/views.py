# encoding:utf-8
import re
import logging

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext

from models import *
import parser

class TextForm(forms.Form):
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'rows':'10', 'cols':'80'}))
class MatchTextForm(forms.Form):
    source = forms.CharField(label="", widget=forms.Textarea(attrs={'rows':'15', 'cols':'80'}))

def index(request):
    t = Tournament.objects.order_by('-id')
    if t.count()>0:
        t = t[0]
        match_count = t.match_set.count()
        try:
            ranking = t.ranking()
        except Exception as e:
            ranking = None
            logging.error(unicode(e))
        return render_to_response("index.html",
                              {'tournament':t, 'match_count':match_count, 'ranking':ranking
                              }, RequestContext(request))
    else:
        return render_to_response("index.html", {}, RequestContext(request))

@permission_required('game.change_tournament')
def tournament_edit(request, tid, text_status="", addmatch_status="", match_text=""):
    t = Tournament.objects.get(id=tid)
    match_count = t.match_set.count()
    form_text = TextForm(initial={'text':t.text})
    form_match = MatchTextForm(initial={'source':match_text})
    p_list = t.participants.all()
    return render_to_response("tedit.html", 
                              {'tournament':t, 'match_count':match_count, 
                              'form_text':form_text, 'text_status':text_status, 
                              'form_match':form_match, 'addmatch_status':addmatch_status,
                              'participation_list': p_list,
                              }, RequestContext(request))

def tournament_matches(request, tid):
    t = Tournament.objects.get(id=tid)
    return render_to_response("matches.html", {'tournament':t,'matches':t.match_set.all()}, RequestContext(request))
    
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
    count = 0
    for record in parse_blocks(source):
        tournament.addMatch(record)
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
