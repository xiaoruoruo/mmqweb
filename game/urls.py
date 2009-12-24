from django.conf.urls.defaults import *

urlpatterns = patterns('', 
                       (r'^$',  'mmqweb.game.views.index'), 
                       (r'^tournament/(?P<tid>\d+)/edit$',  'mmqweb.game.views.tournament_edit'), 
                       (r'^tournament/(?P<tid>\d+)/matches$',  'mmqweb.game.views.tournament_matches'), 
                       (r'^tournament/(?P<tid>\d+)/text$',  'mmqweb.game.views.tournament_edit_text'), 
                       (r'^tournament/(?P<tid>\d+)/addmatches$',  'mmqweb.game.views.tournament_add_matches'), 
                       (r'^tournament/(?P<tid>\d+)/addp$',  'mmqweb.game.views.tournament_add_participation'), 
                       )
