 
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
     * make input types to a bootstrap form control.
     */
	function makeBootstrapFom(){
        $("form :input").each(function(){
            if($(this).attr("type") != "submit"){
                $(this).addClass("form-control");
            }
        });
    
    }
