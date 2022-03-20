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
