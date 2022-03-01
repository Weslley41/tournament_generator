from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from core.models import Tournament, Team, Battle

def index(request):

	return render(request, 'index.html')


def tournament(request, id):
	tournament_obj = get_object_or_404(Tournament, id=id)
	rounds = Battle.objects.values_list('round').filter(tournament=tournament_obj).distinct()
	context = {
		'tournament': tournament_obj,
		'rounds': [],
	}

	for round in rounds:
		battles = Battle.objects.filter(tournament=tournament_obj, round=round[0])
		context['rounds'].append({
			"round": round[0],
			"ladoA": battles[:len(battles) // 2],
			"ladoB": battles[len(battles) // 2:],
		})

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


def battle_infos(request, id):
	battle = get_object_or_404(Battle, id=id).battleToJSON()

	context = {
		'battle': battle,
	}

	return JsonResponse(context)


def error404(request, exception):
	return render(request, 'tournament_not_found.html')
