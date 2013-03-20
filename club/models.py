# encoding: utf8
import datetime

from django.db import models
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization

from xpinyin import Pinyin
pinyin = Pinyin()

# Changing the models here will impact the revisions

class Member(models.Model):
    name  = models.CharField(max_length=50)
    male  = models.BooleanField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    affiliation = models.CharField(max_length=20, null=True, blank=True)
    weight = models.FloatField(default=0.0)
    balance = models.FloatField(default=0.0)
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s (balance: %.2f)' % (self.name, self.balance)

    @property
    def index(self):
        return ''.join(pinyin.get_initials(c) for c in self.name)

    @property
    def sex(self):
        return self.male and u'男' or u'女'

    def is_low_balance(self):
        return self.balance <= 0


class Activity(models.Model):
    member = models.ForeignKey(Member)
    # 算几次
    weight = models.FloatField(default=1.0)
    date   = models.DateField(default=datetime.date.today())

    cost   = models.FloatField(blank=True)
    deposit= models.FloatField(null=True, blank=True)

    def __unicode__(self):
        s = u'%s * %.1f @ %s' % (self.member.name, self.weight, self.date)
        s += u' -￥%d' % self.cost
        if self.deposit:
            s += u' +￥%d' % self.deposit
        return s

class MemberResource(ModelResource):
    class Meta:
        queryset = Member.objects.filter(hidden=False).order_by('-weight')
        resource_name = 'member'
        fields = ['name', 'male', 'hidden']
        limit = 0
        include_resource_uri = True

        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()

    index = fields.CharField(attribute='index', readonly=True)
    balance = fields.CharField(attribute='balance', readonly=True)
    weight = fields.CharField(attribute='weight', readonly=True)

