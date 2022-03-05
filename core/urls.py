from django.urls import path
from django.views import defaults

from .views import index, tournament, tournament_edit, battle_infos
from .tournament_actions import *

urlpatterns = [
	path('', index),
	path('tournament/create/<str:name>', create_tournament),
	path('tournament/<int:id>', tournament),
	path('tournament/<int:id>/knockout', tournament),
	path('tournament/<int:id>/delete', tournament_delete),
	path('tournament/<int:id>/edit', tournament_edit),
	path('tournament/<int:id>/generate/league', generate_league),
	path('tournament/<int:id>/generate/knockout', generate_knockout),
	path('tournament/<int:id>/edit/insert_team/<str:name>', insert_team),
	path('tournament/<int:tournament_id>/edit/remove_team/<int:team_id>', remove_team),
	path('tournament/<int:tournament_id>/battle/<int:battle_id>/scores/team1=<int:team_1_score>&team2=<int:team_2_score>', set_scores_battle),
	path('tournament/<int:tournament_id>/next_round', next_round),
	path('tournament/<int:tournament_id>/final', end_tournament),

	path('battle/<int:id>', battle_infos),
]
