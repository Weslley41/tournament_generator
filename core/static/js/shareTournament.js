function copyLink() {
	let link = document.getElementById("link-to-share-tournament");
	link.select();
	document.execCommand("copy");

	let modalBody = document.getElementById("modal-body-share-tournament");
	let info = document.createElement("p");
	info.className = "alert alert-info";
	info.innerHTML = "Link copied to clipboard";
	modalBody.appendChild(info);
}

function saveImage(id, type, step=0) {
	let btnSaveImage = document.getElementById("btnSaveImage");
	btnSaveImage.classList.add('disabled');
	let request = new XMLHttpRequest();
	let url;
	if (type == "knockout") {
		url = `/tournament/${id}/image/knockout/${step}`;
	} else {
		url = `/tournament/${id}/image/league`;
	}
	request.open("GET", url, true);
	request.send();

	request.onreadystatechange = function() {
		if (request.readyState == 4 && request.status == 200) {
			let link = document.createElement("a");
			link.href = 'data:image/png;base64,' + request.responseText;
			link.download = "tournament-" + type + "-" + id + ".jpg";
			link.click();
			btnSaveImage.classList.remove('disabled');
		}
	}
}
