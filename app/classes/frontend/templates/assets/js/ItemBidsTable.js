
// User Information tabel
// Add, Delete, and Edit Users
$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip();
	var actions = $("table td:last-child").html();
	// Delete row on delete button click
	$(document).on("click", ".delete", function(){
        var request = fetch("", {
			method: "DELETE",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({"item_id": $(this).parents("tr").attr("id")})
		});
		location.reload()
    });
});
