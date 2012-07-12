from django.conf.urls.defaults import *
from django.conf.urls.static import static
from club.models import MemberResource

member_resource = MemberResource()

urlpatterns = patterns('',
                       (r'^api/', include(member_resource.urls)),
                       ) + \
                static('/', document_root='/Users/xrsun/Programs/mmqweb/club/templates')
