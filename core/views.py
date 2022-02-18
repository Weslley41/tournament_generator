from django.shortcuts import render, redirect

from core.models import Tournament, Team

def index(request):

	return render(request, 'index.html')


def tournament(request, id):
	try:
		tournament_obj = Tournament.objects.get(id=id)
	except Tournament.DoesNotExist:
		return render(request, 'tournament_not_found.html')

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

	return render(request, 'tournament.html', context)


def create_tournament(request, name):
	tournament_obj = Tournament(name=name)
	tournament_obj.save_tournament()
	
	return redirect(f'/tournament/{tournament_obj.id}')


def insert_team(request, id, name):
	"""
		Create a new team
		...
		Parameters:
		(string) name_team: team name
	"""

	try:
		tournament_obj = Tournament.objects.get(id=id)
		team = Team(name=name, tournament=tournament_obj)
		team.save_team()

		return redirect(f'/tournament/{id}')
	except Tournament.DoesNotExist:
		return render(request, 'tournament_not_found.html')


def remove_team(request, tournament_id, team_id):
	"""
		Remove a team
		...
		Parameters:
		(int) tournament_id: tournament id
		(int) team_id: team id
	"""

	try:
		tournament_obj = Tournament.objects.get(id=tournament_id)
		team = Team.objects.get(id=team_id)
		team.delete()

		return redirect(f'/tournament/{tournament_id}')
	except Tournament.DoesNotExist:
		return render(request, 'tournament_not_found.html')
