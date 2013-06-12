from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource

from club.models import Member

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
    balance = fields.FloatField(attribute='balance', readonly=True)
    weight = fields.FloatField(attribute='weight', readonly=True)


