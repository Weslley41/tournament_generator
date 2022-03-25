function editBattle(game) {
	let scoreTeam1 = document.getElementById("inputScoreTeam1").value;
	let scoreTeam2 = document.getElementById("inputScoreTeam2").value;

	let battleUpdate = new XMLHttpRequest();
	battleUpdate.open('GET', `battle/${game}/scores/team1=${scoreTeam1}&team2=${scoreTeam2}`, true);
	battleUpdate.send();

	battleUpdate.onload = function() {
		if (battleUpdate.status == 200) {
			let teams = document.querySelectorAll(`#game-${game} #team_score`);
			teams[0].innerText = scoreTeam1;
			teams[1].innerText = scoreTeam2;
			document.getElementById('btnCloseEditBattle').click();
		}
	}
}

function setEditBattleValues(game) {
	let battleRequest = new XMLHttpRequest();
	battleRequest.open('GET', 'battle/' + game, true);
	battleRequest.send()

	battleRequest.onload = function() {
		response = JSON.parse(battleRequest.responseText).battle;

		let nameTeam1 = document.getElementById('nameTeam1');
		nameTeam1.innerText = response.team_1;
		let nameTeam2 = document.getElementById('nameTeam2');
		nameTeam2.innerText = response.team_2;
		let scoreTeam1 = document.getElementById('inputScoreTeam1');
		scoreTeam1.value = response.team_1_score;
		let scoreTeam2 = document.getElementById('inputScoreTeam2');
		scoreTeam2.value = response.team_2_score;
		let btnSaveBattleChanges = document.getElementById('btnSaveBattleChanges');
		btnSaveBattleChanges.setAttribute('onclick', 'editBattle(' + game + ')');
	}
}
