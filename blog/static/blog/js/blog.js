 
$( document ).ready(function() {
	/**
	 * needed for csrftoken
	 * @name: (string) cookiename
	 * @TODO: add to seperate 'tools.js' module
	 */
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	/**
	 * collect form data
	 */
	function getCommentFormData(){
		// collect data
		var name = $('input#id_name').val();
		var email = $('input#id_email').val();
		var website = $('input#id_website').val();
		var comment = $("textarea#id_comment").val();
		var entry_id = $("#context-data").attr('data');
		var csrftoken = getCookie('csrftoken');
		var data = {
			name: name,
			email: email,
			comment: comment,
			website: website,
			entry_id: entry_id,
			csrfmiddlewaretoken: csrftoken,
		}
		return data;
	}

	function applyCSS(){
		$("input#id_captcha_1").prop('required',true);
		$("input#id_name").attr('placeholder', 'name *');
		$("input#id_email").attr('placeholder', 'e-mail *');
		$("input#id_website").attr('placeholder', 'http://website');
		$("div#comment_form input").attr('class', 'form-control');
		$("div#comment_form textarea").attr('class', 'form-control');
		$("textarea#id_comment").attr('placeholder', 'your comment ... *');
		$("textarea#id_comment").attr('rows', '3');
		$("img.captcha").attr('class', 'thumbnail');

		function func_add_errors(e) {
			var func =  function(jdata){
				var error = jdata[e.target.name];
				if ( error ) {
					$("#"+e.target.name+"_error").html(error);
					$("#id_"+e.target.name).addClass("input-error");

				}else{
					$("#"+e.target.name+"_error").html("");
					$("#id_"+e.target.name).removeClass("input-error");

				}
			}
			return func
		}
		function func_check_form(e) {
			var func = function(e){
				$.ajax({
					method: "POST",
					data: getCommentFormData(),
					url: "/blog/comment/form/check/",
					success: func_add_errors(e),
				});
			};
			return func(e);
		}
		$('div#comment_form input').keyup(func_check_form);
		$('div#comment_form input').focusout(func_check_form);
		$('div#comment_form textarea').focusout(func_check_form);
		$('div#comment_form textarea').keyup(func_check_form); 
	} //applyCSS

	function setCSSandJS(){
		applyCSS();
		$('#comment_submit').click(function(e){
				// trigger keyup to trigger error check
				$("div#comment_form input").keyup();
				$("div#comment_form textarea").keyup();
				//wait till changes made
				//sleep(5); //TODO: 
				penis();
				//check for errors
				var errors_len = 0;
				$('.form-error').each( function (){
					var l =  $.trim($(this).html()).length;
					errors_len = errors_len + l;
				});
				if(errors_len == 0){
					// maybe call captcha view
					var data = getCommentFormData();
					$.ajax({
						method: "POST",
						url: "/blog/comment/form/",
						data: data,
						success: function(response_html) {
							$("div#comment_form").html(response_html);
							setCSSandJS(); },

					});
				}

				return false; // avoid to execute the actual form submit
			}); //click
		} // setCSSandJS
		
		/* *** MAIN *** */
		// add comment form on button click
		$('#btn-write-comment').click(function(e){

			var comment_from_div = $("div#comment_form");
			var csrf_token = getCookie('csrftoken');
			console.log(csrf_token);
			// if no form there -> empty div -> add/load form
			if($.trim(comment_from_div.html()).length == 0){
				$.ajax({
					method: "POST",
					url: "/blog/comment/form/",
					data: { csrfmiddlewaretoken: csrf_token, },
					success: function(response_html) {
						$("div#comment_form").html(response_html);
						setCSSandJS();
					}, // success
				}); //ajax
			}else{ // hide form if it already exists
				comment_from_div.hide();
				$("button#btn-write-comment").click(function(){
					$("div#comment_form").toggle();
				});
			}
		});


	}); // ready
