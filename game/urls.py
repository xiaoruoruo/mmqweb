from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$',  'game.views.index'),
                       (r'^tournament/(?P<tid>\d+)/$',  'game.views.tournament_index'),
                       (r'^tournament/(?P<tid>\d+)/edit$',  'game.views.tournament_edit'),
                       (r'^tournament/(?P<tid>\d+)/text$',  'game.views.tournament_edit_text'),
                       (r'^tournament/(?P<tid>\d+)/addmatches$',  'game.views.tournament_add_matches'),
                       (r'^tournament/(?P<tid>\d+)/addp$',  'game.views.tournament_add_participation'),
                       (r'^mg/(?P<mgid>\d+)/matches$',  'game.views.matches'),
                       (r'^mg/(?P<mgid>\d+)/runranking$',  'game.views.ranking_run'),
                       (r'^ranking/(?P<ranking_id>\d+)/$', 'game.views.ranking_index'),
                       (r'^ranking/(?P<ranking_id>\d+)/(?P<name>\w+)/$', 'game.views.ranking_person'),
                       )
