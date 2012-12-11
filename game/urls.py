from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$',  'game.views.index'),
                       (r'^login$', 'game.views.login_user'),
                       (r'^del_match/(?P<match_id>\d+)/$', 'game.views.del_match'),
                       (r'^(?P<tname>\w+)/$',  'game.views.tournament_index'),
                       (r'^(?P<tname>\w+)/edit$',  'game.views.tournament_edit'),
                       (r'^(?P<tname>\w+)/text$',  'game.views.tournament_edit_text'),
                       (r'^(?P<tname>\w+)/addmatches$',  'game.views.tournament_add_matches'),
                       (r'^(?P<tname>\w+)/addp$',  'game.views.tournament_add_participation'),
                       (r'^mg/(?P<mgid>\d+)/matches$',  'game.views.matches'),
                       (r'^mg/(?P<mgid>\d+)/runranking$',  'game.views.ranking_run'),
                       (r'^ranking/(?P<ranking_id>\d+)/$', 'game.views.ranking_index'),
                       (r'^ranking/(?P<ranking_id>\d+)/(?P<name>\w+)/$', 'game.views.ranking_person'),
                       )
