from django.conf.urls.defaults import *

urlpatterns = patterns('', 
                       (r'^$',  'mmqweb.fight.views.index'), 
                       (r'^submit$',  'mmqweb.fight.views.submit'), 
                       )