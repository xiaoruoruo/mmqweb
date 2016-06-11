# encoding: utf8
from models import *

from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User

from datetime import datetime
import random

class YssyRegistrationForm(forms.Form):
    yssyid = forms.CharField(label="水源ID", max_length=12)

def register_yssy(request):
    text = u''
    if request.method == 'POST':
        form = YssyRegistrationForm(request.POST)
        if form.is_valid():
            yssyid = form.cleaned_data['yssyid']
            if User.objects.filter(username=yssyid):
                text = u"该ID已经注册"
            else:
                r = YssyRegistration(yssyid=yssyid,date=datetime.now())
                r.code = ''.join(str(random.randint(0,9)) for i in range(6))
                r.save()
                user = User.objects.create_user(r.yssyid, "%s@bbs.sjtu.edu.cn" % r.yssyid, r.code)
                user.save()
                text = u"已收到您的请求，请耐心等候，稍候会你的密码将躺在站内信里"
    else:
        form = YssyRegistrationForm()

    return render_to_response("register_yssy.html",
            {
                'form':form,
                'text':text,
            })

def submit(request):
    if request.method != 'POST':
        raise Http404
    ip = request.META['HTTP_X_REAL_IP']
    json = request.POST.keys()[0]
    r = GameRecord(ip=ip, json=json)
    r.save()
    return HttpResponse(status=200)

@permission_required('namebook.change_entity')
def label_entity_types(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Bad Request")
    try:
        for key, value in request.POST.iteritems():
            if key.startswith('pt'):
                eid = int(key[2:])
                e = Entity.objects.get(id=eid)
                if value[0] == 'M':
                    e.type = Entity.Man
                elif value[0] == 'F':
                    e.type = Entity.Woman
                else:
                    raise
                e.save()
    except:
        return HttpResponseBadRequest("Bad Request")

    return redirect(request.POST['next'])
