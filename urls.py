from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login'), 
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/mmqweb/'}), 
    (r'^mmqweb/', include('mmqweb.fight.urls')),
    (r'^mmqweb/down/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/xrsun/mmqweb/down'}),
    #(r'^mmqweb/', include('mmqweb.game.urls')),
    #(r'^mmqweb/media/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': settings.TEMPLATE_DIRS[0]}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
