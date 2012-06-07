from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import os
PROJECT_ROOT = os.path.dirname(__file__)

import django
admin_media_url = settings.STATIC_URL.lstrip('/') + 'admin/(?P<path>.*)$'
admin_media_path = os.path.join(django.__path__[0], 'contrib', 'admin', 'static', 'admin')

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^' + admin_media_url , 'django.views.static.serve', {
        'document_root': admin_media_path,
        }),

    (r'^accounts/login/$', 'game.views.login_user'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/game/'}),
    (r'^game/', include('game.urls')),
    (r'^nb/', include('namebook.urls')),
    (r'^', include('fight.urls')),
    #(r'^mmqweb/', include('namebook.urls')),
    (r'^down/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(PROJECT_ROOT,'static')}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(PROJECT_ROOT,'static')}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
