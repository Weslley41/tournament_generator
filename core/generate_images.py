from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import Tournament, Battle, Team

import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def generate_league_image(request, tournament_id):
	""" Generate an image of league tournaments """
	IMAGE = Image.open('core/static/images/ranking_table.jpg')
	FONT = "core/static/font/Rajdhani-Regular.ttf"
	TITLE_FONT = ImageFont.truetype(FONT, size=68)
	ROUND_FONT = ImageFont.truetype(FONT, size=76)
	TABLE_LABELS_FONT = ImageFont.truetype(FONT, size=30)
	TEAM_FONT = ImageFont.truetype(FONT, size=28)
	POSITION_X = {
		"Pos": 100,
		"Team": 170,
		"W": 500,
		"D": 570,
		"L": 640,
		"F": 710,
		"A": 780,
		"+/-": 850,
		"PTS": 920,
	}

	draw = ImageDraw.Draw(IMAGE)
	tournament_obj = get_object_or_404(Tournament, id=tournament_id)
	teams = Team.objects.filter(tournament=tournament_obj).order_by('-points', '-goals_difference', '-goals_scored')[:20]

	draw.text((90, 50), tournament_obj.name, font=TITLE_FONT, fill=(255, 255, 255))
	draw.text((950, 60), str(tournament_obj.current_round).rjust(2, '0'), font=TITLE_FONT, fill=(255, 255, 255))
	y_pos = 154
	for label, x_pos in POSITION_X.items():
		draw.text((x_pos, y_pos), label, font=TABLE_LABELS_FONT, fill=(255, 255, 255))
	y_pos += 50

	for position, team in enumerate(teams):
		draw.text((POSITION_X["Pos"], y_pos), str(position + 1).rjust(2, '0'), font=TEAM_FONT, fill=(255, 255, 255))
		draw.text((POSITION_X["Team"], y_pos), team.name, font=TEAM_FONT, fill=(255, 255, 255))
		draw.text((POSITION_X["W"], y_pos), str(team.wins).rjust(2, '0'), font=TEAM_FONT, fill=(255, 255, 255))
		draw.text((POSITION_X["D"], y_pos), str(team.draws).rjust(2, '0'), font=TEAM_FONT, fill=(255, 255, 255))
		draw.text((POSITION_X["L"], y_pos), str(team.defeats).rjust(2, '0'), font=TEAM_FONT, fill=(255, 255, 255))
		draw.text((POSITION_X["F"], y_pos), str(team.goals_scored).rjust(2, '0'), font=TEAM_FONT, fill=(255, 255, 255))
		draw.text((POSITION_X["A"], y_pos), str(team.goals_conceded).rjust(2, '0'), font=TEAM_FONT, fill=(255, 255, 255))
		draw.text((POSITION_X["+/-"], y_pos), str(team.goals_difference).rjust(2, '0'), font=TEAM_FONT, fill=(255, 255, 255))
		draw.text((POSITION_X["PTS"], y_pos), str(team.points).rjust(2, '0'), font=TEAM_FONT, fill=(255, 255, 255))
		y_pos += 40

	return HttpResponse(image_to_base64(IMAGE), content_type="image/jpeg")


def generate_knockout_image(request, tournament_id, step):
	""" Generate an image of knockout tournaments """
	IMAGE = {
		"16": Image.open('core/static/images/16-finals.jpg'),
		"8": Image.open('core/static/images/quarter-finals.jpg'),
	}
	FONT = "core/static/font/Rajdhani-Regular.ttf"
	TITLE_FONT = ImageFont.truetype(FONT, size=68)
	TEAM_FONT = ImageFont.truetype(FONT, size=28)
	GAME_FONT = ImageFont.truetype(FONT, size=12)
	FINAL_TEAM_FONT = ImageFont.truetype(FONT, size=36)
	FINAL_GAME_FONT = ImageFont.truetype(FONT, size=20)
	TEAMS_DISTANCE = {
		"x_to_teams": 11,
		"x_to_scores": 157,
		"y_to_team_1": 28,
		"y_to_team_2": 78,
	}
	TEAMS_FINAL_DISTANCE = {
		"x_to_teams": 11,
		"x_to_scores": 248,
		"y_to_team_1": 46,
		"y_to_team_2": 121,
	}
	POSITION_X = {
		"16_1_A": 51,
		"16_2_A": 275,
		"16_3_A": 331,
		"16_1_B": 833,
		"16_2_B": 607,
		"16_3_B": 552,
		"16_final": 393,
		"8_1_A": 91,
		"8_2_A": 146,
		"8_1_B": 792,
		"8_2_B": 737,
		"8_final": 393,
	}
	POSITION_Y = {
		"16_1_1": 403,
		"16_1_2": 528,
		"16_1_3": 653,
		"16_1_4": 778,
		"16_2_1": 466,
		"16_2_2": 716,
		"16_3_1": 591,
		"16_final": 225,
		"8_1_1": 362,
		"8_1_2": 612,
		"8_2_1": 487,
		"8_final": 454,
	}

	draw = ImageDraw.Draw(IMAGE[step])
	tournament_obj = get_object_or_404(Tournament, id=tournament_id)
	rounds = Battle.objects.values_list('round').filter(tournament=tournament_obj).distinct().order_by('round')
	draw.text((90, 50), tournament_obj.name, font=TITLE_FONT, fill=(255, 255, 255))

	n_round = 0
	for round in rounds:
		battles = Battle.objects.filter(tournament=tournament_obj, round=round[0]).order_by('game')
		if (battles.count() > int(step) // 2):
			continue
		n_round += 1
		battle_to_switch_bracket = battles.count() // 2

		for n_battle, battle in enumerate(battles):
			if (battles.count() == 1):
				bracket = step + '_final'
				game = step + '_final'
				final = True
			elif (n_battle >= battle_to_switch_bracket):
				final = False
				bracket = step + '_' + str(n_round) + '_B'
				game = step + '_' + str(n_round) + '_' + str(n_battle % battle_to_switch_bracket + 1)
			else:
				final = False
				bracket = step + '_' + str(n_round) + '_A'
				game = step + '_' + str(n_round) + '_' + str(n_battle + 1)

			battle_fonts = (FINAL_GAME_FONT, FINAL_TEAM_FONT) if final else (GAME_FONT, TEAM_FONT)
			distance = TEAMS_FINAL_DISTANCE if final else TEAMS_DISTANCE
			x_teams = POSITION_X[bracket] + distance["x_to_teams"]
			x_scores = POSITION_X[bracket] + distance["x_to_scores"]
			y_team_1 = POSITION_Y[game] + distance["y_to_team_1"]
			y_team_2 = POSITION_Y[game] + distance["y_to_team_2"]

			draw.text((POSITION_X[bracket], POSITION_Y[game]), 'Game ' + str(battle.game), font=battle_fonts[0], fill=(255, 255, 255))
			draw.text((x_teams, y_team_1), battle.team_1.name, font=battle_fonts[1], fill=(255, 255, 255))
			draw.text((x_teams, y_team_2), battle.team_2.name, font=battle_fonts[1], fill=(255, 255, 255))
			if (not battle.editable):
				draw.text((x_scores, y_team_1), str(battle.team_1_score).rjust(2, '0'), font=battle_fonts[1], fill=(255, 255, 255))
				draw.text((x_scores, y_team_2), str(battle.team_2_score).rjust(2, '0'), font=battle_fonts[1], fill=(255, 255, 255))

	return HttpResponse(image_to_base64(IMAGE[step]), content_type="image/jpeg")


def image_to_base64(image):
	buffer = BytesIO()
	image.save(buffer, format="JPEG")
	img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

	return img_str
