from django.conf.urls import url
from game import views

urlpatterns = [
    url(r'^$',  views.index),
    url(r'^login$', views.login_user, name='game_login_user'),
    url(r'^del_match/(?P<match_id>\d+)/$', views.del_match, name='game_del_match'),
    url(r'^(?P<tname>\w+)/$',  views.tournament_index, name='game_tournament_index'),
    url(r'^(?P<tname>\w+)/edit$',  views.tournament_edit, name='game_tournament_edit'),
    url(r'^(?P<tname>\w+)/text$',  views.tournament_edit_text, name='game_tournament_edit_text'),
    url(r'^(?P<tname>\w+)/addmatches$',  views.tournament_add_matches, name='game_tournament_add_matches'),
    url(r'^(?P<tname>\w+)/addp$',  views.tournament_add_participation, name='game_tournament_add_participation'),
    url(r'^mg/(?P<mgid>\d+)/matches$',  views.matches, name='game_matches'),
    url(r'^mg/(?P<mgid>\d+)/runranking$',  views.ranking_run, name='game_ranking_run'),
    url(r'^ranking/(?P<ranking_id>\d+)/$', views.ranking_index, name='game_ranking_index'),
    url(r'^ranking/(?P<ranking_id>\d+)/(?P<name>\w+)/$', views.ranking_person, name='game_ranking_person'),
]
