function createTournament() {
	if (!event.key || event.key === 'Enter') {
		let tournament_name = document.getElementById('inputTournamentName').value;
		open('tournament/create/' + tournament_name, '_self');
	}
}

function deleteTournament(id) {
	document.cookie = 'tournament=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/';
	open('/tournament/' + id + '/delete', '_self');
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

function setCookie(id) {
	/* Set cookie and exclude expired tournaments */
	let timeToExpire = new Date();
	let days = 3;
	timeToExpire.setTime(timeToExpire.getTime() + (days * 24 * 60 * 60 * 1000));
	document.cookie = `tournament=${id}; expires=${timeToExpire.toUTCString()}; path=/`;

	let request = new XMLHttpRequest();
	request.open('GET', '/check_expired_tournaments', true);
	request.send();
}

function getCookie() {
	try {
		let cookies = document.cookie.split(';');
		let cookie = cookies.find(cookie => cookie.includes('tournament'));
		let tournament_id = cookie.split('=')[1];

		let request = new XMLHttpRequest();
		request.open('GET', '/tournament/' + tournament_id + '/tournament_infos', true);
		request.send();

		request.onreadystatechange = function() {
			if (request.DONE === request.readyState) {
				document.getElementById('boxCreateTournament').classList.add('visually-hidden');
				let btnDelete = document.getElementById('btn-delete-tournament')
				btnDelete.setAttribute('onclick', `deleteTournament(${tournament_id})`);
				// Create link for tournament
				let body = document.querySelector('body');
				let title = document.createElement('h3');
				title.className = 'ms-2';
				title.innerHTML = 'Tournament active';
				body.appendChild(title);
				let card = document.createElement('div');
				card.className = 'card col-lg-3 ms-2';
				let bodyCard = document.createElement('div');

				let tournament = JSON.parse(request.responseText);
				bodyCard.innerHTML = `
				<h5 class="card-header d-flex justify-content-between">
					${tournament.name}
					<i class="bi bi-trash" data-bs-toggle="modal" data-bs-target="#deleteTournament" style="cursor: pointer"></i>
				</h5>
				<p class="card-body">
				Type: ${tournament.type}<br/>
				Round: ${tournament.current_round}<br/>
				Status: ${tournament.status}<br/>
				${tournament.count_teams} teams</p>
				<div class="card-footer d-flex justify-content-around">
					<a href="tournament/${tournament_id}/edit" class="btn btn-primary">Edit tournament</a>
					<a href="tournament/${tournament_id}" class="btn btn-primary">Go to tournament</a>
				</div>
				`

				card.appendChild(bodyCard);
				body.appendChild(card);
			}
		}
	} catch (error) {
		console.log('No tournament active');
	}
}
