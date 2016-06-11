from django.conf.urls import include, url
from django.conf.urls.static import serve
from django.conf import settings
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

import django
admin_media_url = settings.STATIC_URL.lstrip('/') + 'admin/(?P<path>.*)$'
admin_media_path = os.path.join(django.__path__[0], 'contrib', 'admin', 'static', 'admin')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^' + admin_media_url , serve, {'document_root': admin_media_path}),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^game/', include('game.urls')),
    url(r'^club/', include('club.urls')),
    url(r'^nb/', include('namebook.urls')),
    url(r'^(?P<path>robots\.txt)$', serve, {'document_root': PROJECT_ROOT}),
    url(r'^', include('fight.urls')),
    #(r'^mmqweb/', include('namebook.urls')),
    url(r'^down/(?P<path>.*)$', serve, {'document_root': os.path.join(PROJECT_ROOT,'static')}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': os.path.join(PROJECT_ROOT,'static')}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]
