from django.db import models

class Tournament(models.Model):
	"""
		Tournament model
		id: primary key
		name: tournament name
	"""

	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	status = models.CharField(max_length=100, default='not started')
	current_round = models.IntegerField(default=0)
	type = models.CharField(max_length=100, default='knockout')


	def __str__(self):
		return self.name


	def change_status(self, status):
		"""
			Change tournament status
			...
			Parameters:
			(string) status: new status
		"""
		self.status = status
		self.save()


	def change_current_round(self):
		"""
			Change current round
		"""
		self.current_round += 1
		self.save()

		return self.current_round


class Team(models.Model):
	"""
		Team model
		...
		Parameters:
		(string) name: team name
		(object) tournament: tournament object
		Attributes:
		id: primary key
		name: team name
		tournament: foreign key to Tournament model
		wins: number of wins
		draws: number of draws
		defeats: number of defeats
		goals_scored: number of goals scored
		goals_conceded: number of goals conceded
		goals_difference: number of goals difference

		Methods:
		add_win: add win to team
		add_draw: add draw to team
		add_defeat: add defeat to team
		set_goals_scored: set goals scored
		set_goals_conceded: set goals conceded
		set_goals_difference: set goals difference
	"""

	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
	points = models.IntegerField(default=0)
	wins = models.IntegerField(default=0)
	draws = models.IntegerField(default=0)
	defeats = models.IntegerField(default=0)
	goals_scored = models.IntegerField(default=0)
	goals_conceded = models.IntegerField(default=0)
	goals_difference = models.IntegerField(default=0)
	false_team = models.BooleanField(default=False)

	def __str__(self):
		return self.name


	def add_win(self):
		"""
			Add win to team
		"""
		self.wins += 1
		self.points += 3
		self.save()


	def add_draw(self):
		"""
			Add draw to team
		"""
		self.draws += 1
		self.points += 1
		self.save()


	def add_defeat(self):
		"""
			Add defeat to team
		"""
		self.defeats += 1
		self.save()


	def set_goals_scored(self, goals):
		"""
			Set goals scored
			Parameters:
			goals(int): number of goals scored
		"""
		self.goals_scored += goals
		self.save()


	def set_goals_conceded(self, goals):
		"""
			Set goals conceded
			Parameters:
			goals(int): number of goals conceded
		"""
		self.goals_conceded += goals
		self.save()


	def set_goals_difference(self):
		"""
			Set goals difference
		"""
		self.goals_difference = self.goals_scored - self.goals_conceded
		self.save()


	def remove_team(self):
		"""
			Remove team
		"""
		self.delete()


class Battle(models.Model):
	"""
		Battle model
		...
		Parameters:
		(integer) round: round number
		(integer) game: round number
		(object) tournament: tournament object
		(object) team_1: team object
		(object) team_2: team object
		Attributes:
		game: primary key
		round: number of round
		team_1: foreign key to Team model
		team_2: foreign key to Team model
		team_1_score: score of team_1
		team_2_score: score of team_2

		Methods:
		set_team_1_score: set score of team_1
		set_team_2_score: set score of team_2
		end_battle: end battle and distributes the score
	"""

	id = models.AutoField(primary_key=True)
	tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
	game = models.IntegerField()
	round = models.IntegerField()
	team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_1', default=None)
	team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_2', default=None)
	team_1_score = models.IntegerField(default=0)
	team_2_score = models.IntegerField(default=0)
	editable = models.BooleanField(default=True)
	winner = models.CharField(max_length=8, default='None')

	def __str__(self):
		return f'Round {self.round} - Game {self.game}\n{self.team_1.name} {self.team_1_score}x{self.team_2_score} {self.team_2.name}'


	def set_scores(self, team_1_score, team_2_score):
		"""
			Set scores of battle
			Parameters:
			team_1_score(int): score of team_1
			team_2_score(int): score of team_2
		"""
		self.team_1_score = team_1_score
		self.team_2_score = team_2_score
		self.save()


	def end_battle(self):
		"""
			End battle and distributes the score
			Returns:
			None for draw or (object) for winner team
		"""
		if (self.team_1_score > self.team_2_score):
			self.team_1.add_win()
			self.team_2.add_defeat()
			self.winner = "team_1"
		elif (self.team_1_score < self.team_2_score):
			self.team_1.add_defeat()
			self.team_2.add_win()
			self.winner = "team_2"
		else:
			self.team_1.add_draw()
			self.team_2.add_draw()
			self.winner = 'None'

		# Goals scored
		self.team_1.set_goals_scored(self.team_1_score)
		self.team_2.set_goals_scored(self.team_2_score)
		# Goals conceded
		self.team_1.set_goals_scored(self.team_2_score)
		self.team_2.set_goals_scored(self.team_1_score)
		# Goals difference
		self.team_1.set_goals_difference()
		self.team_2.set_goals_difference()

		self.editable = False
		self.team_1.save()
		self.team_2.save()
		self.save()

		return self.get_winner()


	def get_winner(self):
		"""
		Get winner team
		Returns:
		None for draw or (object) for winner team
		"""
		if (self.team_1_score > self.team_2_score):
			return self.team_1
		elif (self.team_1_score < self.team_2_score):
			return self.team_2
		else:
			return None


	def battleToJSON(self):
		"""
			Returns battle as json
		"""

		return {
			'id': self.id,
			'game': self.game,
			'round': self.round,
			'team_1': self.team_1.name,
			'team_2': self.team_2.name,
			'team_1_score': self.team_1_score,
			'team_2_score': self.team_2_score,
			'editable': self.editable
		}


class unknownTeam():
	"""
		Unknown team model
	"""
	id = None
	name = "Unknown"
	tournament = None
	wins = None
	draws = None
	defeats = None
	goals_scored = None
	goals_conceded = None
	goals_difference = None
	false_team = None


class unknownBattle():
	"""
		Unknown battle model
	"""
	id = None
	tournament = None
	game = 0
	round = 0
	team_1 = unknownTeam()
	team_2 = unknownTeam()
	team_1_score = 0
	team_2_score = 0
	editable = False
	winner = "None"
