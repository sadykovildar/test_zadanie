function SendRequest(){			//testing ajax + django
		alert("!");
		$.ajax({
			url: "test/",
			success: function(response){
				alert(response);
				$('#response').html(response);
			}
		});
	};

function SortNotes(){
	var sort = $("#sort");
	var s_category = $("#sort_category").val();
	var s_cret = $("#sort_cret").val();
	
	$.ajax({
            url: "sort/",
			type: 'post',
            data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value'), s_category:s_category, s_cret:s_cret},
            success: function(data){
				var html = "";
				var notes = data["notes"]
                var n = notes.length;
				
				for (var i=0; i<n; i++) {
					html = html +
							"<div id=\"list_of_notes\" style=\"border: 3px solid #E0E0E0; border-radius: 4px; padding: 3px; margin: 4px 0px\">" +
							"<a href=\"/note/" + notes[i]["uuid"] + "/\">" + notes[i]["header"] + "</a>" +
							"<label style=\"float: right; color: blue; font-size: 16px\" onclick=\"SetNoteChosen('" + notes[i]["uuid"] + "')\" id=" + notes[i]["uuid"] + ">";
							if(notes[i]["chosen"]) {
									html=html + "<span style\"color: blue\">Избранная</span>";
								} else{
									html=html + "<span style=\"color: #A90000\">Не избранная</span>";
								}
								
					html = html + "</label><br>" +
							"<span style=\"float:left; color: green\">"+ notes[i]["category"]+"</span><br>" + notes[i]["text"] + "<br><br>"+
							"<button onclick=\"DelNote('"+ notes[i]["uuid"]+ "')\" class=\"label round\" style=\"font-size: 14px\" id=\"del\">Удалить</button>" +
							"<span style=\"float:right\">"+notes[i]["pub_date"]+"</span></div>";
				}
				$('#response').html(html);
			}
		});


};

function CreateFieldsForSearch(){
        
            var cretery = $("#search_category").val()
            if (cretery == 1) {
                html = "<output style='color: green; font-size: 25px'></output> " +
                "<input type='text' id='datepicker' value='Нажми' style='width: 100px' onmouseover='DatepickerOnFocus()'> " +
                "<button class='button' id='search' name='1' onclick='FunctionByCriterions()'>Поиск</button> " +
                "<button class='button' id='exit_search'>Отмена</button> " +
                "<output style='color: green; font-size: 25px'></output>"
            }
            if (cretery == 2) {
                html = "<output style='color: green; font-size: 25px'></output> " +
                "<input type='text' id='search_data'> " +
                "<button class='button' id='search' name='2' onclick='FunctionByCriterions()'>Поиск</button> " +
                "<button class='button' id='exit_search'>Отмена</button> " +
                "<output style='color: green; font-size: 25px'></output>"
            }
            if (cretery == 3) {
                html = "<output style='color: green; font-size: 25px'></output> " +
                "<select id='search_data' size='1' class='tiny_stile' style='width: 175px;'> " +
                $("#id_category").html() +
                "</select><br> <button class='button' id='search' name='3' onclick='FunctionByCriterions()'>Поиск</button> " +
                "<button class='button' id='exit_search'>Отмена</button> " +
                "<output style='color: green; font-size: 25px'></output>"
            }
            if (cretery == 4) {
                html = "<output style='color: green; font-size: 25px'></output> " +
                "<label>Избранное :<input type='checkbox' id='search_fav_checkbox'></label><br> " +
                "<button class='button' id='search' name='4' onclick='FunctionByCriterions()'>Поиск</button> " +
                "<button class='button' id='exit_search'>Отмена</button> " +
                "<output style='color: green; font-size: 25px'></output>"
            }
            $('#search_field').html(html);
        
    };
	
	 function FunctionByCriterions(){	
		
        var id_of_criterion = document.getElementById('search').getAttribute('name');
		
        if(id_of_criterion == 1){
            var data = $("#datepicker").val();
        }
        if(id_of_criterion == 2){
            var data = $("#search_data").val();
        }
		if(id_of_criterion == 3){
			var data = $("#search_data option:selected").text();
		}
        if(id_of_criterion == 4) {
			//var data = document.getElementById('search_fav_checkbox').value;
            var data = $("#search_fav_checkbox").prop("checked");
			data = data ? 1 : 2
        }
		//alert("data = " + data);
		
		
        if(data != "Нажми" && data != ""){
            $.ajax({
                url: "search/",
                type: "POST",
                data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value'), id_of_criterion:id_of_criterion, data:data },
                success: function (data) {
				
				var html = "";
				var notes = data["notes"]
                var n = notes.length;
				for (var i=0; i<n; i++) {
                    html = html +
							"<div id=\"list_of_notes\" style=\"border: 3px solid #E0E0E0; border-radius: 4px; padding: 3px; margin: 4px 0px\">" +
							"<a href=\"/note/" + notes[i]["uuid"] + "/\">" + notes[i]["header"] + "</a>" +
							"<label style=\"float: right; color: blue; font-size: 16px\" onclick=\"SetNoteChosen('" + notes[i]["uuid"] + "')\" id=" + notes[i]["uuid"] + ">";
							if(notes[i]["chosen"]) {
									html=html + "<span style\"color: blue\">Избранная</span>";
								} else{
									html=html + "<span style=\"color: #A90000\">Не избранная</span>";
								}
								
					html = html + "</label><br>" +
							"<span style=\"float:left; color: green\">"+ notes[i]["category"]+"</span><br>" + notes[i]["text"] + "<br><br>"+
							"<button onclick=\"DelNote('"+ notes[i]["uuid"]+ "')\" class=\"label round\" style=\"font-size: 14px\" id=\"del\">Удалить</button>" +
							"<span style=\"float:right\">"+notes[i]["pub_date"]+"</span></div>";

				}
				$('#response').html(html);
				
				
                }
        });
		
        }

    }; 
	
    function DatepickerOnFocus(){
        $("#datepicker").datepicker();
        $("#datepicker").datepicker($.datepicker.regional["ru"]);
    };

	
function DelNote(note_uuid){
	result = confirm("Вы действительно хотите удалить эту заметку?");
	
	
	if(result){
		
		$.ajax({
			url: "del/",
			type: "POST",
			data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value'),  note_uuid:note_uuid },
			success: function (data) {
		
			var html = "";
			var notes = data["notes"]
			var n = notes.length;
			for (var i=0; i<n; i++) {
				html = html +
							"<div id=\"list_of_notes\" style=\"border: 3px solid #E0E0E0; border-radius: 4px; padding: 3px; margin: 4px 0px\">" +
							"<a href=\"/note/" + notes[i]["uuid"] + "/\">" + notes[i]["header"] + "</a>" +
							"<label style=\"float: right; color: blue; font-size: 16px\" onclick=\"SetNoteChosen('" + notes[i]["uuid"] + "')\" id=" + notes[i]["uuid"] + ">";
							if(notes[i]["chosen"]) {
									html=html + "<span style\"color: blue\">Избранная</span>";
								} else{
									html=html + "<span style=\"color: #A90000\">Не избранная</span>";
								}
								
					html = html + "</label><br>" +
							"<span style=\"float:left; color: green\">"+ notes[i]["category"]+"</span><br>" + notes[i]["text"] + "<br><br>"+
							"<button onclick=\"DelNote('"+ notes[i]["uuid"]+ "')\" class=\"label round\" style=\"font-size: 14px\" id=\"del\">Удалить</button>" +
							"<span style=\"float:right\">"+notes[i]["pub_date"]+"</span></div>";

			}
			$('#response').html(html);
			
			
			}
		});
	}
	
};

function SetNoteChosen(note_uuid){
	
	$.ajax({
			url: "setChosen/",
			type: "POST",
			data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value'),  note_uuid:note_uuid },
			success: function (data) {
				id = '#' + note_uuid;
				html = ""
				if(data=="True"){
					html = "<span style='color: blue'>Избранная	</span>";
				} else {
					html = "<span style='color: #A90000'>Не избранная</span>";
				}				
				$(id).html(html);
			
			
			}
		});
};

