 
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

  function getCSRF(){
    return getCookie('csrftoken');
  }

  /**
   * check the whole form (all input field).
   */
  function checkForm(){
  }
  
  /** 
   * check a singel input field.
   * @input_element (dom element) ie: $('input#id_website')
   */
  function checkInput(input_element){
		var data = {[input_element.name]: input_element.value,
        csrfmiddlewaretoken: getCSRF(), };
    return $.post({
      data: data,
      url: '/blog/comment/form/check/',
			success: function (json_respons){
				showInputErrors(input_element, json_respons);
      },
    });
  }

  /**
   * adds/ removes errors to html error div.
   * @param: {DOM el} input_element ie: $('input#id_email').
   * @param: {json} json_response ajax response with field errors.
   */
  function showInputErrors(input_element, json_response){
    var element_name = input_element.name;
    var error = json_response[element_name];
    if ( error ) {
      $("#"+element_name+"_error").html(error);
      $("#id_"+element_name).addClass("input-error");
    }else{
      $("#"+element_name+"_error").html("");
      $("#id_"+element_name).removeClass("input-error");
    }
  }
  
  function showFrom(){}
  function adjustStyleBehaviour(){}

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

		var func_check = function(e){ return checkInput(e.target);};

		$('div#comment_form input').keyup(func_check);
		$('div#comment_form input').focusout(func_check);
		$('div#comment_form textarea').focusout(func_check);
		$('div#comment_form textarea').keyup(func_check); 
	} //applyCSS

	function setCSSandJS(){
		applyCSS();
		$('#comment_submit').click(function(e){
			 
			var ajax_deferred =new Array();
			// trigger keyup to trigger error check
			$("div#comment_form input, div#comment_form textarea").each(function(){
				ajax_deferred.push(checkInput($(this)[0]));
			});
			// $("div#comment_form input:text, div#comment_form textarea").ajaxStop(function(){
			var err = 0;
			$.when.apply($, ajax_deferred).done(function(r){
				$('.form-error').each( function (){
					var l = $.trim($(this).html()).length;
					err +=l;
				});
				if(err==0){
					// maybe call captcha view
					var data = getCommentFormData();
					return $.post({
						url: "/blog/comment/form/",
						data: data,
						success: function(response_html) {
							$("div#comment_form").html(response_html);
							setCSSandJS(); },
					});
				}
			});
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
