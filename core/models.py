from django.db import models

class Tournament(models.Model):
	"""
		Tournament model
		id: primary key
		name: tournament name
	"""

	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


	def save_tournament(self):
		"""
			Save a tournament
		"""
		self.save()


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
	wins = models.IntegerField(default=0)
	draws = models.IntegerField(default=0)
	defeats = models.IntegerField(default=0)
	goals_scored = models.IntegerField(default=0)
	goals_conceded = models.IntegerField(default=0)
	goals_difference = models.IntegerField(default=0)

	def __str__(self):
		return self.name


	def add_win(self):
		"""
			Add win to team
		"""
		self.wins += 1
		self.save()


	def add_draw(self):
		"""
			Add draw to team
		"""
		self.draws += 1
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
		self.goals_scored = goals
		self.save()


	def set_goals_conceded(self, goals):
		"""
			Set goals conceded
			Parameters:
			goals(int): number of goals conceded
		"""
		self.goals_conceded = goals
		self.save()


	def set_goals_difference(self):
		"""
			Set goals difference
		"""
		self.goals_difference = self.goals_scored - self.goals_conceded
		self.save()


	def save_team(self):
		"""
			Save team
		"""
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

	def __str__(self):
		return f'Round {self.round} - Game {self.game}\n{self.team_1.name} {self.team_1_score}x{self.team_2_score} {self.team_2.name}'


	def set_team_1_score(self, score):
		"""
			Set score of team_1
			Parameters:
			score(int): score of team_1
		"""
		self.team_1_score = score
		self.save()


	def set_team_2_score(self, score):
		"""
			Set score of team_2
			Parameters:
			score(int): score of team_2
		"""
		self.team_2_score = score
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
			winner = self.team_1
		elif (self.team_1_score < self.team_2_score):
			self.team_1.add_defeat()
			self.team_2.add_win()
			winner = self.team_2
		else:
			self.team_1.add_draw()
			self.team_2.add_draw()
			winner = None

		self.team_1.save()
		self.team_2.save()

		return winner


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


	def save_battle(self):
		"""
			Save battle
		"""
		self.save()
