function createTournament() {
	tournament_name = document.getElementById('inputTournamentName').value;
	open('tournament/create/' + tournament_name, '_self');
}
