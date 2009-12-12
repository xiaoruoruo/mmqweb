from django.conf.urls.defaults import *

urlpatterns = patterns('', 
                       (r'^$',  'mmqweb.game.views.index'), 
                       (r'^tournament/(?P<tid>\d+)/edit$',  'mmqweb.game.views.tournament_edit'), 
                       (r'^tournament/(?P<tid>\d+)/matches$',  'mmqweb.game.views.tournament_matches'), 
                       )
