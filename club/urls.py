import os

from django.conf.urls import url, include
from django.conf.urls.static import static
from tastypie.api import Api
from club.resources import MemberResource
from club import views

v1_api = Api(api_name='')
v1_api.register(MemberResource())

urlpatterns = [
    url(r'^$', views.index, name='club_index'),
    url(r'^api', include(v1_api.urls)),
    url(r'^checkin$', views.checkin, name='club_checkin'),
    url(r'^new_member$', views.new_member, name='club_new_member'),
    url(r'^balance_sheet$', views.balance_sheet, name='club_balance_sheet'),
    url(r'^activity/(?P<name>.+)$', views.activity_sheet, name='club_activity_sheet'),
    url(r'^date/(?P<act_date>[\d-]+)/activity$', views.activity_by_date, name='club_activity_by_date'),
    url(r'^overall$', views.activity_overall, name='club_activity_overall'),
] + static('/', view=views.csrf_serve, document_root=os.path.join(os.path.dirname(__file__), 'static'))
