from django.shortcuts import redirect, get_object_or_404

from .models import Tournament, Team, Battle
from .brackets_len import brackets_len

def create_tournament(request, name):
	tournament_obj = Tournament(name=name)
	tournament_obj.save_tournament()
	
	return redirect(f'/tournament/{tournament_obj.id}/edit')


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

	generate_battles(list_teams, tournament_obj)
	return redirect(f'/tournament/{id}/knockout')


def generate_battles(list_teams, tournament_obj):
	"""
		Generates the battles
		...
		Parameters:
			(list) list_teams: list of teams
			(object) tournament_obj: tournament object
	"""
	from random import choice

	count_teams = len(list_teams)
	last_round = Battle.objects.values_list('round').filter(tournament=tournament_obj).distinct().last()
	round = last_round[0] + 1 if last_round else 1
	last_game = Battle.objects.values_list('game').filter(tournament=tournament_obj).last()
	last_game = last_game[0] if last_game else 0

	for game in range(1, count_teams // 2 + 1):
		team1 = list_teams.pop()
		team2 = choice(list_teams)
		# While team1 and team2 are 'None'
		while (team1.name == team2.name):
			team2 = choice(list_teams)
		list_teams.remove(team2)

		battle = Battle(round=round, game=last_game + game, tournament=tournament_obj, team_1=team1, team_2=team2)
		battle.save_battle()

		if ('None' in [team1.name, team2.name]):
			battle.set_team_1_score(score=3) if team1.name != 'None' else battle.set_team_2_score(score=3)
			battle.end_battle()
