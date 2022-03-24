from django.urls import path
from django.views import defaults

from .views import (
	index, tournament, tournament_edit, tournament_battles, tournament_brackets, tournament_table
)
from .generate_images import generate_knockout_image, generate_league_image

from .tournament_actions import (
	check_expired_tournaments, create_tournament, tournament_delete,
	battle_infos, insert_team, remove_team, generate_league, generate_knockout,
	generate_first_battles_knockout, set_scores_battle, next_round, next_round_knockout,
	next_round_league, end_tournament)


urlpatterns = [
	# Pages
	## Global
	path('', index),
	path('tournament/<str:id>/edit', tournament_edit),
	path('check_expired_tournaments', check_expired_tournaments),
	## Knockout
	path('tournament/<str:id>/knockout/brackets', tournament_brackets),
	path('tournament/<str:id>/knockout/battles', tournament_battles),
	## League
	path('tournament/<str:id>/league/battles', tournament_battles),

	# Actions
	## Global
	path('tournament/create/<str:name>', create_tournament),
	path('tournament/<str:id>', tournament),
	path('tournament/<str:id>/delete', tournament_delete),
	path('tournament/<str:id>/edit/insert_team/<str:name>', insert_team),
	path('tournament/<str:tournament_id>/edit/remove_team/<int:team_id>', remove_team),
	path('tournament/<str:tournament_id>/<str:tournament_type>/battle/<int:game>', battle_infos),
	path('tournament/<str:tournament_id>/<str:tournament_type>/battle/<int:game>/scores/team1=<int:team_1_score>&team2=<int:team_2_score>', set_scores_battle),
	path('tournament/<str:tournament_id>/<str:tournament_type>/next_round', next_round),
	## Knockout
	path('tournament/<str:id>/knockout', tournament),
	path('tournament/<str:id>/generate/knockout', generate_knockout),
	path('tournament/<str:tournament_id>/knockout/final', end_tournament),
	path('tournament/<str:tournament_id>/image/knockout/<str:step>', generate_knockout_image),
	## League
	path('tournament/<str:id>/league', tournament),
	path('tournament/<str:id>/generate/league', generate_league),
	path('tournament/<str:id>/league/table', tournament_table),
	path('tournament/<str:tournament_id>/image/league', generate_league_image),
]
