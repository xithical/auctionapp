// User Information tabel
// Add, Delete, and Edit Users
$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip();
	var actions = $("table td:last-child").html();
	// Append table with add row form on add new button click
    $(".add-new").click(async function(){
		$(this).attr("disabled", "disabled");
		var index = $("table tbody tr:last-child").index();
		const req = await fetch("/admin/users/get_roles");
		var response = await req.json()
			.then(data => {
				roles = data.roles
			});
		var roles_list = ""
		roles.forEach(element => {
			var out = '<option value=' + element.type_id + '>' + element.type_name + '</option>';
			var roles_out = roles_list + out;
			roles_list = roles_out;
		});
        var row = '<tr>' +
            '<td><input name="user_firstname" type="text" class="form-control" id="UserFirst"></td>' +
            '<td><input name="user_lastname" type="text" class="form-control" id="UserLast"></td>' +
            '<td><input name="user_email" type="text" class="form-control" id="UserEmail"></td>' +
			'<td><input name="user_phone" type="text" class="form-control" id="UserPhone"></td>' +
            '<td><input name="user_password" type="text" class="form-control" id="UserPassword"></td>' +
            '<td><select name="type_id" class="form-control" id="UserType">'+ roles_list +'</select></td>' +
			'<td>'+
			'<a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a>' +
			'<a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a>' +
			'<a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a>' +
			'</td>' +
        '</tr>';
    	$("table").append(row);		
		$("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
        $('[data-toggle="tooltip"]').tooltip();
    });
    
	// Add row on add button click
	$(document).on("click", ".add", function(){
		var empty = false;
		var input = $(this).parents("tr").find('input[type="text"]');
        input.each(function(){
			if(!$(this).val() && !($(this).attr("name") == "user_password")){
				$(this).addClass("error");
				empty = true;
			} else{
                $(this).removeClass("error");
            }
		});
		$(this).parents("tr").find(".error").first().focus();
		if(!empty){
			var type_id = $('#UserType').find(":selected").val();
			var data = {
				"type_id": type_id
			}
			input.each(function(){
				data[$(this).attr("name")] = $(this).val()
			});
			if(!$(this).parents("tr").attr("edit_mode") == true){
				var request = fetch("/admin/users", {
					method: "POST",
					headers: {
						"Content-Type": "application/json"
					},
					body: JSON.stringify(data)
				});
			}
			else{
				data["user_id"] = $(this).parents("tr").attr("id");
				var request = fetch("/admin/users", {
					method: "PUT",
					headers: {
						"Content-Type": "application/json"
					},
					body: JSON.stringify(data)
				});
			};
		};	
		location.reload()	
    });
	// Edit row on edit button click
	$(document).on("click", ".edit", async function(){	
        $(this).parents("tr").find("td:not(:last-child)").each(async function(){
			if($(this).attr("input-mode") == "input"){
				$(this).html('<input name="' + $(this).attr("name") + '" type="text" class="form-control" value="' + $(this).text() + '">');
			}
			else if(($(this).attr("input-mode") == "select") && ($(this).attr("name") == "type_id")){
				var value = $(this).val
				const req = await fetch("/admin/users/get_roles");
				var response = await req.json()
					.then(data => {
						roles = data.roles
					});
				var roles_list = ""
				var type_id = $(this).attr("type_id");
				roles.forEach(element => {
					if(type_id == element.type_id){
						var out = '<option value=' + element.type_id + ' selected>' + element.type_name + '</option>';
					}
					else{
						var out = '<option value=' + element.type_id + '>' + element.type_name + '</option>';

					};
					var roles_out = roles_list + out;
					roles_list = roles_out;
				});	
				$(this).html('<select name="type_id" class="form-control" id="UserType">' + roles_list + '</select>');
			};
		});		
		$(this).parents("tr").find(".add, .edit").toggle();
		$(this).parents("tr").attr("edit_mode", true);
		$(".add-new").attr("disabled", "disabled");
    });
	// Delete row on delete button click
	$(document).on("click", ".delete", function(){
        var request = fetch("/admin/users", {
			method: "DELETE",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({"user_id": $(this).parents("tr").attr("id")})
		});
		location.reload()
    });
});
