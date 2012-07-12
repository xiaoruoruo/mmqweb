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
    weight = models.FloatField()

    def __unicode__(self):
        return self.name

    @property
    def index(self):
        return ''.join(pinyin.get_initials(c) for c in self.name)


class Activity(models.Model):
    member = models.ForeignKey(Member)
    weight = models.FloatField(default=1.0)
    date   = models.DateField()

class MemberResource(ModelResource):
    class Meta:
        queryset = Member.objects.order_by('-weight')
        resource_name = 'member'
        fields = ['name', 'weight']
        limit = 0
    index = fields.CharField(attribute='index')

