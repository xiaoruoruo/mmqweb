import os

from django.conf.urls.defaults import patterns, include
from django.conf.urls.static import static
from tastypie.api import Api
from club.models import MemberResource, ActivityResource

v1_api = Api(api_name='')
v1_api.register(MemberResource())
v1_api.register(ActivityResource())

urlpatterns = patterns('',
                       (r'^api', include(v1_api.urls)),
                       (r'^checkin$', 'club.views.checkin'),
                       (r'^new_member$', 'club.views.new_member'),
                       (r'^balance_sheet$', 'club.views.balance_sheet'),
                       (r'^activity/(?P<name>.+)$', 'club.views.activity_sheet'),
                       ) + \
                static('/', document_root=os.path.join(os.path.dirname(__file__), 'templates'))
