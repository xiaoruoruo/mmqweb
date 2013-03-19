import os

from django.conf.urls import patterns, include
from django.conf.urls.static import static
from tastypie.api import Api
from club.models import MemberResource

v1_api = Api(api_name='')
v1_api.register(MemberResource())

urlpatterns = patterns('',
                       (r'^$', 'club.views.index'),
                       (r'^api', include(v1_api.urls)),
                       (r'^checkin$', 'club.views.checkin'),
                       (r'^new_member$', 'club.views.new_member'),
                       (r'^balance_sheet$', 'club.views.balance_sheet'),
                       (r'^activity/(?P<name>.+)$', 'club.views.activity_sheet'),
                       (r'^overall$', 'club.views.activity_overall'),
                       (r'^mmqweb.db$', 'club.views.dump_db'),
                       ) + \
                static('/', view='club.views.csrf_serve', document_root=os.path.join(os.path.dirname(__file__), 'static'))

