from django.shortcuts import render, redirect, get_object_or_404

from core.models import Tournament, Team, Battle
from core.brackets_len import brackets_len

def index(request):

	return render(request, 'index.html')


def create_tournament(request, name):
	tournament_obj = Tournament(name=name)
	tournament_obj.save_tournament()
	
	return redirect(f'/tournament/{tournament_obj.id}/edit')


def tournament(request, id):
	tournament_obj = get_object_or_404(Tournament, id=id)
	battles = Battle.objects.filter(tournament=tournament_obj)

	context = {
		'tournament': tournament_obj,
		'battles': battles,
	}

	return render(request, 'tournament.html', context)


def tournament_edit(request, id):
	tournament_obj = get_object_or_404(Tournament, id=id)

	try:
		teams = Team.objects.filter(tournament=tournament_obj)
		count_teams = len(teams)
	except Team.DoesNotExist:
		count_teams, teams = 0, []

	context = {
		'tournament': tournament_obj,
		'count_teams': count_teams,
		'teams': teams,
	}

	return render(request, 'tournament_edit.html', context)


def tournament_delete(request, id):
	"""
		Delete a tournament
		...
		Parameters:
		(int) id: tournament id
	"""

	tournament_obj = get_object_or_404(Tournament, id=id)
	tournament_obj.delete()

	return redirect('/')


def generate_league(request, id):
	pass


def generate_knockout(request, id):
	"""
		Generate a knockout tournament
		...
		Parameters:
		(int) id: tournament id
	"""
	from random import shuffle
	tournament_obj = get_object_or_404(Tournament, id=id)
	list_teams = Team.objects.filter(tournament=id)

	if len(list_teams) < 4:
		return redirect(f'/tournament/{id}/edit')

	count_teams = len(list_teams)
	len_brackets = brackets_len(count_teams)

	for i in range (len_brackets - count_teams):
		Team(name='None', tournament=tournament_obj).save_team()
	list_teams = list(Team.objects.filter(tournament=id))
	shuffle(list_teams)

	for i in range(0, len_brackets, 2):
		team1 = list_teams[i]
		team2 = list_teams[i + 1]
		new_battle = Battle(round=1, game=1, tournament=tournament_obj, team_1=team1, team_2=team2)
		new_battle.save_battle()

	return redirect(f'/tournament/{id}/all')


def insert_team(request, id, name):
	"""
		Create a new team
		...
		Parameters:
		(string) name_team: team name
	"""

	tournament_obj = get_object_or_404(Tournament, id=id)
	team = Team(name=name, tournament=tournament_obj)
	team.save_team()

	return redirect(f'/tournament/{id}/edit')


def remove_team(request, tournament_id, team_id):
	"""
		Remove a team
		...
		Parameters:
		(int) tournament_id: tournament id
		(int) team_id: team id
	"""

	tournament_obj = get_object_or_404(Tournament, id=tournament_id)
	team = Team.objects.get(id=team_id)
	team.delete()

	return redirect(f'/tournament/{tournament_id}/edit')


def error404(request, exception):
	return render(request, 'tournament_not_found.html')
