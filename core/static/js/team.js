function addTeam() {
	let team_name = document.getElementById('inputTeamName').value;
	open(window.location.href + '/insert_team/' + team_name, '_self');
}

function removeTeam(team_id) {
	open(window.location.href + '/remove_team/' + team_id, '_self');
}
