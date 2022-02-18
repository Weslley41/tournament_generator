from django.urls import path

from .views import index, create_tournament, tournament, insert_team, remove_team

urlpatterns = [
	path('', index),
	path('tournament/create/<str:name>', create_tournament),
	path('tournament/<int:id>', tournament),
	path('tournament/<int:id>/insert_team/<str:name>', insert_team),
	path('tournament/<int:tournament_id>/remove_team/<int:team_id>', remove_team),
]
