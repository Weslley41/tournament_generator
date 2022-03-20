from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

from .models import Tournament, Team, Battle
from .brackets_len import brackets_len


def generate_id():
	""" Generate a random id """
	from random import choice
	from string import digits

	id = int(''.join([ choice(digits) for i in range(16)]))
	while Tournament.objects.filter(id=id).exists():
		id = ''.join([ choice(digits) for i in range(16)])

	return id


def check_expired_tournaments(request):
	""" Check and delete expired tournaments """

	from datetime import datetime, timedelta, timezone

	expire_date = (datetime.now() - timedelta(days=3)).replace(tzinfo=timezone.utc)
	tournaments_expired = Tournament.objects.filter(last_accessed__lte=expire_date).delete()

	return HttpResponse(status=200)


def create_tournament(request, name, owner):
	id = generate_id()
	tournament_obj = Tournament(id=id, name=name, owner=owner)
	tournament_obj.save()

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


def tournament_infos(request, id):
	"""
	Returns the infos of a tournament
	...
	Parameters:
		(int) id: tournament id
	Returns:
		(dict) tournament: name, type, status, current_round, count_teams
	"""

	tournament_obj = get_object_or_404(Tournament, id=id)
	context = {
		'name': tournament_obj.name,
		'type': tournament_obj.type,
		'status': tournament_obj.status,
		'current_round': tournament_obj.current_round,
		'count_teams': Team.objects.filter(tournament=id).count(),
	}

	return JsonResponse(context)


def battle_infos(request, tournament_id, tournament_type, game):
	"""
		Get battle infos
		...
		Parameters:
			(int) id: battle id
			(int) game: game number

		Returns:
			(JsonResponse) battle infos
	"""

	tournament_obj = get_object_or_404(Tournament, id=tournament_id)
	battle = get_object_or_404(Battle, tournament=tournament_obj, game=game).battleToJSON()

	context = {
		'battle': battle,
	}

	return JsonResponse(context)


def insert_team(request, id, name):
	"""
		Create a new team
		...
		Parameters:
		(string) name_team: team name
	"""

	tournament_obj = get_object_or_404(Tournament, id=id)
	team = Team(name=name, tournament=tournament_obj)
	team.save()

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
	"""
		Generate a league tournament
	"""

	from random import shuffle

	tournament_obj = get_object_or_404(Tournament, id=id)
	tournament_obj.type = 'league'
	tournament_obj.save()

	list_teams = list(Team.objects.filter(tournament=tournament_obj))
	n_rounds = len(list_teams) - 1
	shuffle(list_teams)

	round = game = 1
	battles = {}
	# First half
	for i in range(n_rounds):
		battles[f'round_{round}'] = []
		for j in range(len(list_teams) // 2):
			team_1 = list_teams[j]
			team_2 = list_teams[-(j + 1)]
			battle = Battle(round=round, game=game, tournament=tournament_obj, team_1=team_1, team_2=team_2)
			battles[f'round_{round}'].append(battle)
			battle.save()
			game += 1

		round += 1
		list_teams.append(list_teams.pop(0))

	# Second half
	for n_round in range(1, n_rounds + 1):
		for first_battle in battles[f'round_{n_round}']:
			team_1 = first_battle.team_2
			team_2 = first_battle.team_1
			battle = Battle(round=round, game=game, tournament=tournament_obj, team_1=team_1, team_2=team_2)
			battle.save()
			game += 1

		round += 1

	tournament_obj.change_status('running')
	tournament_obj.change_current_round()
	return redirect(f'/tournament/{id}/league/battles')


def generate_knockout(request, id):
	"""
		Prepare a knockout tournament for first round
		...
		Parameters:
		(int) id: tournament id
	"""

	tournament_obj = get_object_or_404(Tournament, id=id)
	list_teams = Team.objects.filter(tournament=id)

	if len(list_teams) < 4:
		return redirect(f'/tournament/{id}/edit')

	count_teams = len(list_teams)
	len_brackets = brackets_len(count_teams)

	# Add false teams, if necessary
	for i in range (len_brackets - count_teams):
		Team(name='No Team', tournament=tournament_obj, false_team=True).save()
	list_teams = list(Team.objects.filter(tournament=id))

	generate_first_battles_knockout(list_teams, tournament_obj)
	return redirect(f'/tournament/{id}/knockout')


def generate_first_battles_knockout(list_teams, tournament_obj):
	"""
		Generates the battles of first round
		...
		Parameters:
			(list) list_teams: list of teams
			(object) tournament_obj: tournament object
	"""

	from random import choice

	count_teams = len(list_teams)
	tournament_obj.change_current_round()
	round = tournament_obj.current_round
	last_game = Battle.objects.values_list('game').filter(tournament=tournament_obj).last()
	last_game = last_game[0] if last_game else 0

	for game in range(1, count_teams // 2 + 1):
		team1 = list_teams.pop()
		team2 = choice(list_teams)
		while (team1.false_team and team2.false_team):
			team2 = choice(list_teams)
		list_teams.remove(team2)

		battle = Battle(round=round, game=last_game + game, tournament=tournament_obj, team_1=team1, team_2=team2)
		battle.save()

		if (team1.false_team or team2.false_team):
			battle.set_scores(3, 0) if team2.false_team else battle.set_scores(0, 3)
			battle.end_battle()

		tournament_obj.change_status('running')


def set_scores_battle(request, tournament_id, tournament_type, game, team_1_score, team_2_score):
	"""
		Set the scores of a battle
		...
		Parameters:
			(int) tournament_id: tournament id
			(str) tournament_type: tournament type
			(int) game: game number
			(int) team_1_score: score of team 1
			(int) team_2_score: score of team 2
	"""

	tournament_obj = get_object_or_404(Tournament, id=tournament_id)
	battle = get_object_or_404(Battle, tournament=tournament_obj, game=game)
	if (battle.editable):
		battle.set_scores(team_1_score, team_2_score)

	return HttpResponse(status=200)


def next_round(request, tournament_id, tournament_type):
	"""
		Redirect to the next round
		...
		Parameters:
			(int) tournament_id: tournament id
			(str) tournament_type: tournament type
	"""

	if (tournament_type == 'league'):
		return next_round_league(tournament_id)
	elif (tournament_type == 'knockout'):
		return next_round_knockout(tournament_id)


def next_round_knockout(tournament_id):
	"""
		Generates the next round of knockout tournament
		...
		Parameters:
			(int) tournament_id: tournament id
	"""

	tournament_obj = get_object_or_404(Tournament, id=tournament_id)
	current_round = tournament_obj.current_round
	battles = Battle.objects.filter(tournament=tournament_obj, round=current_round).order_by('game')
	if (None not in [battle.get_winner() for battle in battles]):
		tournament_obj.change_current_round()
		new_round = tournament_obj.current_round
		current_game = battles.last().game + 1

		for i in range(0, battles.count(), 2):
			team_1 = battles[i].end_battle()
			team_2 = battles[i + 1].end_battle()
			new_battle = Battle(round=new_round, game=current_game + i, tournament=tournament_obj,
													team_1=team_1, team_2=team_2)
			new_battle.save()

		tournament_obj.change_status('running')

	return redirect(f'/tournament/{tournament_id}/knockout/battles')


def next_round_league(tournament_id):
	"""
		Ends the battles of the round
		...
		Parameters:
			(obj) tournament: a tournament object
	"""

	tournament_obj = get_object_or_404(Tournament, id=tournament_id)
	current_round = tournament_obj.current_round

	battles = Battle.objects.filter(tournament=tournament_obj, round=current_round).order_by('game')
	for battle in battles:
		battle.end_battle()

	n_rounds = (Team.objects.filter(tournament=tournament_obj).count() - 1) * 2
	if (current_round == n_rounds):
		tournament_obj.change_status('ended')

		return redirect(f'/tournament/{tournament_id}/league/table')
	else:
		tournament_obj.change_current_round()

	return redirect(f'/tournament/{tournament_id}/league/battles')


def end_tournament(request, tournament_id):
	"""
		Ends the tournament
		...
		Parameters:
			(int) id: tournament id
	"""

	tournament_obj = get_object_or_404(Tournament, id=tournament_id)
	current_round = tournament_obj.current_round
	battles = Battle.objects.filter(tournament=tournament_obj, round=current_round).order_by('game')
	for battle in battles:
		battle.end_battle()

	tournament_obj.change_status('ended')

	return redirect(f'/tournament/{tournament_id}/{tournament_obj.type}')
