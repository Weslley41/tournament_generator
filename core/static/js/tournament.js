function createTournament() {
	let tournament_name = document.getElementById('inputTournamentName').value;
	open('tournament/create/' + tournament_name, '_self');
}

function deleteTournament() {
	open('delete', '_self');
}

function generateTournament() {
	let typeTournament = document.querySelector('input[name="typeTournament"]:checked').value;
	open('generate/' + typeTournament, '_self');
}
