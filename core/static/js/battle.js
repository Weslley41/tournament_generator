function editBattle(id) {
	let scoreTeam1 = document.getElementById("inputScoreTeam1").value;
	let scoreTeam2 = document.getElementById("inputScoreTeam2").value;
	
}

function setEditBattleValues(id) {
	let battleRequest = new XMLHttpRequest();
	battleRequest.open('GET', '/battle/' + id, true);
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
		btnSaveBattleChanges.setAttribute('onclick', 'editBattle(' + id + ')');
	}
}
