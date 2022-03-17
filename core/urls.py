from django.urls import path
from django.views import defaults

from .views import index, tournament, tournament_edit, tournament_battles, tournament_brackets, tournament_table
from .tournament_actions import *

urlpatterns = [
	# Pages
	## Global
	path('', index),
	path('tournament/<int:id>/edit', tournament_edit),
	path('check_expired_tournaments', check_expired_tournaments),
	## Knockout
	path('tournament/<int:id>/knockout/brackets', tournament_brackets),
	path('tournament/<int:id>/knockout/battles', tournament_battles),
	## League
	path('tournament/<int:id>/league/battles', tournament_battles),

	# Actions
	## Global
	path('tournament/create/<str:name>', create_tournament),
	path('tournament/<int:id>', tournament),
	path('tournament/<int:id>/delete', tournament_delete),
	path('tournament/<int:id>/edit/insert_team/<str:name>', insert_team),
	path('tournament/<int:tournament_id>/edit/remove_team/<int:team_id>', remove_team),
	path('tournament/<int:id>/tournament_infos', tournament_infos),
	path('tournament/<int:tournament_id>/<str:tournament_type>/battle/<int:game>', battle_infos),
	path('tournament/<int:tournament_id>/<str:tournament_type>/battle/<int:game>/scores/team1=<int:team_1_score>&team2=<int:team_2_score>', set_scores_battle),
	path('tournament/<int:tournament_id>/<str:tournament_type>/next_round', next_round),
	## Knockout
	path('tournament/<int:id>/knockout', tournament),
	path('tournament/<int:id>/generate/knockout', generate_knockout),
	path('tournament/<int:tournament_id>/knockout/final', end_tournament),
	## League
	path('tournament/<int:id>/league', tournament),
	path('tournament/<int:id>/generate/league', generate_league),
	path('tournament/<int:id>/league/table', tournament_table),
]
