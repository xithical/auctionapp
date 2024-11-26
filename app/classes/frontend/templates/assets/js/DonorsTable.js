// Add, Delete, and Edit Users
$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip();
	var actions = $("table td:last-child").html();
	// Append table with add row form on add new button click
    $(".add-new").click(function(){
		$(this).attr("disabled", "disabled");
		var index = $("table tbody tr:last-child").index();
        var row = '<tr>' +
            '<td><input name="UserFirst" type="text" class="form-control" name="UserFirst" id="UserFirst"></td>' +
            '<td><input name="UserLast" type="text" class="form-control" name="UserLast" id="UserLast"></td>' +
            '<td><input name="UserEmail" type="text" class="form-control" name="UserEmail" id="UserEmail"></td>' +
            '<td><input name="UserPhone" type="text" class="form-control" name="UserPhone" id="UserPhone"></td>' +
            '<td><input name="UserCompany" type="text" class="form-control" name="UserCompany" id="UserCompany"></td>' +
           
			'<td>' + actions + '</td>' +
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
			if(!$(this).val()){
				$(this).addClass("error");
				empty = true;
			} else{
                $(this).removeClass("error");
            }
		});
		$(this).parents("tr").find(".error").first().focus();
		if(!empty){
			input.each(function(){
				$(this).parent("td").html($(this).val());
			});			
			$(this).parents("tr").find(".add, .edit").toggle();
			$(".add-new").removeAttr("disabled");
		}		
		if(!$(this).parents("tr").attr("edit_mode") == true){
			var request = $.post({
				url: "/admin/donors",
				data: input.serialize()
			});
		}
		else{
			var data = {
				"donor_id": $(this).parents("tr").attr("id"),
			};
			input.each(function(){
				data[$(this).attr("name")] = $(this).val()
			});
			console.log(data)
			var request = fetch("/admin/donors", {
				method: "PUT",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify(data)
			});
		}
		location.reload()
    });
	// Edit row on edit button click
	$(document).on("click", ".edit", function(){		
        $(this).parents("tr").find("td:not(:last-child)").each(function(){
			$(this).html('<input name="'+ $(this).attr("name") +'" type="'+$(this).attr("type") + '" class="form-control" value="' + $(this).text() + '">');
		});		
		$(this).parents("tr").find(".add, .edit").toggle();
		$(this).parents("tr").attr("edit_mode", true)
		$(".add-new").attr("disabled", "disabled");
    });
	// Delete row on delete button click
	$(document).on("click", ".delete", function(){
        var request = fetch("/admin/donors", {
			method: "DELETE",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({"donor_id": $(this).parents("tr").attr("id")})
		});
		location.reload()
    });
});
