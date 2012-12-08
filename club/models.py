# encoding: utf8
import datetime

from django.db import models
from tastypie.resources import ModelResource
from tastypie import fields

from xpinyin import Pinyin
pinyin = Pinyin()

class Member(models.Model):
    name  = models.CharField(max_length=50)
    male  = models.BooleanField()
    phone = models.CharField(max_length=15, null=True)
    affiliation = models.CharField(max_length=20, null=True)
    weight = models.FloatField(default=0.0)

    balance = models.FloatField(default=0.0)

    def __unicode__(self):
        return u'%s (balance: %.2f)' % (self.name, self.balance)

    @property
    def index(self):
        return ''.join(pinyin.get_initials(c) for c in self.name)

    def is_low_balance(self):
        return self.balance <= 0


class Activity(models.Model):
    member = models.ForeignKey(Member)
    # 算几次
    weight = models.FloatField(default=1.0)
    date   = models.DateField(default=datetime.date.today())

    cost   = models.FloatField()
    deposit= models.FloatField(null=True)

    def __unicode__(self):
        s = u'%s * %.1f @ %s' % (self.member.name, self.weight, self.date)
        s += u' -￥%d' % self.cost
        if self.deposit:
            s += u' +￥%d' % self.deposit
        return s

class MemberResource(ModelResource):
    class Meta:
        queryset = Member.objects.order_by('-weight')
        resource_name = 'member'
        fields = ['name', 'balance']
        limit = 0
        include_resource_uri = False

        # change to SessionAuthentication and DjangoAuthorization once tastypie 0.9.12 is out
        # authentication = Authentication()
        # authorization = Authorization()

    index = fields.CharField(attribute='index')

class ActivityResource(ModelResource):
    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activity'
        list_allowed_methods = ['put']
        detail_allowed_methods = []

