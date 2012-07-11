from django.conf.urls.defaults import *
from club.models import MemberResource

member_resource = MemberResource()

urlpatterns = patterns('',
                       (r'^$',  'club.views.index'),
                       (r'^api/', include(member_resource.urls)),
                       )
