from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login'), 
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/mmqweb/'}), 
    (r'^mmqweb/game/', include('mmqweb.game.urls')),
    (r'^mmqweb/', include('mmqweb.fight.urls')),
    #(r'^mmqweb/', include('mmqweb.namebook.urls')),
    (r'^mmqweb/static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/xrsun/mmqweb/static'}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
