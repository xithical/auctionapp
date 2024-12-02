
// User Information tabel
// Add, Delete, and Edit Users
$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip();
	var actions = $("table td:last-child").html();
	// Append table with add row form on add new button click
    $(".add-new").click(function(){
		$(this).attr("disabled", "disabled");
		var index = $("table tbody tr:last-child").index();
        var row = '<tr>' +
            '<td><input type="text" class="form-control" name="EventName" id="EventName" placeholder="Name of Event"></td>' +
            '<td><input type="datetime-local" class="form-control" name="StartTime" id="StartTime"></td>' +
            '<td><input type="datetime-local" class="form-control" name="EndTime" id="EndTime"></td>' +
            '<td><input type="text" class="form-control" name="EventCode" id="EventCode" placeholder="Leave blank to generate"></td>' +
            
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
		var input = $(this).parents("tr").find('input');
        input.each(function(){
			if(!$(this).val() && !($(this).attr("name") == "EventCode")){
				$(this).addClass("error");
				empty = true;
			} 
			else{
                $(this).removeClass("error");
            };
		});
		$(this).parents("tr").find(".error").first().focus();
		if(!empty){
			input.each(function(){
				$(this).parent("td").html($(this).val());
			});			
			$(this).parents("tr").find(".add, .edit").toggle();
			$(".add-new").removeAttr("disabled");
		};		
		if(!$(this).parents("tr").attr("edit_mode") == true){
			var request = $.post({
				url: "/admin/events",
				data: input.serialize()
			});
		}
		else{
			var data = {
				"event_id": $(this).parents("tr").attr("id"),
			};
			input.each(function(){
				data[$(this).attr("name")] = $(this).val()
			});
			var request = fetch("/admin/events", {
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
        var request = fetch("/admin/events", {
			method: "DELETE",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({"event_id": $(this).parents("tr").attr("id")})
		});
		location.reload()
    });
});
