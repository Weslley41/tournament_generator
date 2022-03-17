from django.shortcuts import render, redirect, get_object_or_404

from core.models import Tournament, Team, Battle, unknownBattle

def index(request):
	""" Index page """
	return render(request, 'index.html')


def tournament(request, id):
	""" Redirect to tournament page	"""

	tournament_obj = get_object_or_404(Tournament, id=id)

	if (tournament_obj.type == 'knockout'):
		return redirect('/tournament/' + str(id) + '/knockout/battles')
	else:
		return redirect('/tournament/' + str(id) + '/league/battles')


def tournament_brackets(request, id):
	""" Tournament brackets page """

	tournament_obj = get_object_or_404(Tournament, id=id)
	tournament_obj.update_last_accessed()
	rounds = Battle.objects.values_list('round').filter(tournament=tournament_obj).distinct().order_by('round')
	context = {
		'tournament': tournament_obj,
		'other_battles': [],
		'rounds': [],
		'current_round': tournament_obj.current_round,
	}

	for round in rounds:
		battles = Battle.objects.filter(tournament=tournament_obj, round=round[0]).order_by('game')

		# Brackets
		if (1 < battles.count() <= 8):
			context['rounds'].append({
				"round": round[0],
				"bracket_A": battles[:len(battles) // 2],
				"bracket_B": battles[len(battles) // 2:],
			})
		elif (battles.count() == 1):
			context['final'] = battles[0]
		else:
			context['other_battles'].append({
				"round": round[0],
				"battles": battles,
			})

		# Battles not defined
		count_battles = battles.count()
		while (count_battles >= 2):
			count_battles = count_battles // 2

			if (count_battles > 1):
				context['rounds'].append({
					"round": 0,
					"bracket_A": [unknownBattle() for j in range(count_battles // 2)],
					"bracket_B": [unknownBattle() for k in range(count_battles // 2)],
				})
			else:
				context['final'] = unknownBattle()

	return render(request, 'tournament_brackets.html', context)


def tournament_battles(request, id):
	""" Tournament battles page """

	tournament_obj = get_object_or_404(Tournament, id=id)
	tournament_obj.update_last_accessed()
	rounds = Battle.objects.values_list('round').filter(tournament=tournament_obj).distinct().order_by('round')

	context = {
		'tournament': tournament_obj,
		'rounds': [],
		'n_rounds': range(1, rounds.count() + 1),
	}

	for round in rounds:
		battles = Battle.objects.filter(tournament=tournament_obj, round=round[0]).order_by('game')
		context['rounds'].append({
			"round": round[0],
			"battles": battles,
		})

	return render(request, 'tournament_battles.html', context)


def tournament_table(request, id):
	""" Tournament tables page """

	tournament_obj = get_object_or_404(Tournament, id=id)
	tournament_obj.update_last_accessed()
	teams = Team.objects.filter(tournament=tournament_obj).order_by('-points', '-goals_difference', '-goals_scored')
	context = {
		'tournament': tournament_obj,
		'teams': [],
	}
	for pos, team in enumerate(teams):
		context['teams'].append({
			'position': pos + 1,
			'team': team,
		})

	return render(request, 'tournament_table.html', context)


def tournament_edit(request, id):
	""" Tournament edit page """

	tournament_obj = get_object_or_404(Tournament, id=id)
	tournament_obj.update_last_accessed()

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


def error404(request, exception):
	""" Error 404 page """

	return render(request, 'tournament_not_found.html')
