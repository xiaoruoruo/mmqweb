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

    def __unicode__(self):
        return self.name

    @property
    def index(self):
        return ''.join(pinyin.get_initials(c) for c in self.name)


class Activity(models.Model):
    member = models.ForeignKey(Member)
    weight = models.FloatField(default=1.0)
    date   = models.DateField(default=datetime.date.today())

    def __unicode__(self):
        return u'%s * %.1f @ %s' % (self.member, self.weight, self.date)

class MemberResource(ModelResource):
    class Meta:
        queryset = Member.objects.order_by('-weight')
        resource_name = 'member'
        fields = ['name']
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

