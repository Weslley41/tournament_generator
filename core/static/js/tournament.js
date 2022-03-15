function createTournament() {
	if (!event.key || event.key === 'Enter') {
		let tournament_name = document.getElementById('inputTournamentName').value;
		open('tournament/create/' + tournament_name, '_self');
	}
}

function deleteTournament() {
	open('delete', '_self');
}

function generateTournament() {
	let typeTournament = document.querySelector('input[name="typeTournament"]:checked').value;
	let btnGenerate = document.getElementById('btn-generate-tournament');
	let btnLoading = document.getElementById('btn-loading');

	btnGenerate.classList.add('visually-hidden');
	btnLoading.classList.remove('visually-hidden');

	open('generate/' + typeTournament, '_self');
}

function nextRound(final=false) {
	open(final ? 'final' : 'next_round', '_self');
}
