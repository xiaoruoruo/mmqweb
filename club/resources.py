from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource

from club.models import Member

class MemberResource(ModelResource):
    class Meta:
        queryset = Member.objects.order_by('-weight')
        resource_name = 'member'
        fields = ['name', 'male', 'hidden', 'hidden_date', 'cost', 'extra']
        limit = 0
        include_resource_uri = True

        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()

    index = fields.CharField(attribute='index', readonly=True)
    balance = fields.FloatField(attribute='balance', readonly=True)
    weight = fields.FloatField(attribute='weight', readonly=True)
    cost = fields.FloatField(attribute='cost', readonly=True)

    def hydrate(self, bundle):
        # Convert the attribute to the field value:
        # We only want to change the override if the inferred value has been
        # changed.
        if bundle.data['cost'] != bundle.obj.cost:
            bundle.obj.cost_override = bundle.data['cost']
        return bundle

