from django.urls import path
from django.views import defaults

from .views import index, create_tournament, tournament, tournament_delete, tournament_edit, generate_league, generate_knockout, insert_team, remove_team

urlpatterns = [
	path('', index),
	path('tournament/create/<str:name>', create_tournament),
	path('tournament/<int:id>', tournament),
	path('tournament/<int:id>/all', tournament),
	path('tournament/<int:id>/delete', tournament_delete),
	path('tournament/<int:id>/edit', tournament_edit),
	path('tournament/<int:id>/generate/league', generate_league),
	path('tournament/<int:id>/generate/knockout', generate_knockout),
	path('tournament/<int:id>/edit/insert_team/<str:name>', insert_team),
	path('tournament/<int:tournament_id>/edit/remove_team/<int:team_id>', remove_team),
]
