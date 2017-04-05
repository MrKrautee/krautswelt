/**
 * set up ajax form.
 *  use as following:
 *    setUpAjaxForm('#form-select', '/url/');
 *    setUpAjaxForm({
 *            url: '/url',
 *            selector: '#form_sel',
 *            onSuccess: function(){}
 *    });
 *    setUpAjaxForm('#form-select', '/url/', {onFieldError: function(){}});
 *
 * @param {string} form_selector - form to validate.
 * @param {string} url - specify the validation server.
 * @param {Object} [options]
 * @param {Object} [options.getFormData] form data,format: return {input_name: input_value,}.
 * @param {boolean} [options.on_typing=true] - validate form on keyup and focusOut.
 * @param {int} [options.stop_typing_delay=1100] - milliseconds.
 * @param {function} [options.onSuccess] - (no parameters) called after the whole form is
 *                                         successfull submitted.
 * @param {function} [options.onFieldError] - (element_name, json.respons)
 *                                            called on each field error.
 *                                            default: indicate the error with
 *                                            bootstrap warnings.
 **/
function setUpAjaxForm(form_selector, url, options){
	var AjaxForm = {
		selector: form_selector,
		url: url,
		on_typing: true,
		stop_typing_delay: 1100,
		/**
		 * adds/ removes errors to html error div.
		 * @param {DOM el} input_element ie: $('input#id_email').
		 * @param {json} json_response ajax response with field errors.
		 */
		onFieldError: function(element_name, json_response){
			var error = json_response[element_name];
			if(error){
				$(this.selector+" #"+element_name+"_help").hide();
				$(this.selector+" #"+element_name+"_errors").html(error);
				$(this.selector+" #id_"+element_name).parent().addClass("has-error");;
				$(this.selector+" #id_"+element_name).next().addClass("glyphicon-remove");
			}else{
				$(this.selector+" #"+element_name+"_help").show();
				$(this.selector+" #"+element_name+"_errors").html("");
				$(this.selector+" #id_"+element_name).parent().removeClass("has-error");
				$(this.selector+" #id_"+element_name).parent().addClass("has-success");
				$(this.selector+" #id_"+element_name).next().removeClass("glyphicon-remove");
				$(this.selector+" #id_"+element_name).next().addClass("glyphicon-ok");
			}
		},
		getFormData: function(){
			var data = { };
			$(this.selector+" :input").each(function(){
				if($(this).attr("type") != "submit" ){
					data[$(this).attr('name')] = $(this).val();
				}
			});
			return data
		},
		onSuccess: function(){
		},
		/**
		 * check a singel input field.
		 * @input_element (dom element) ie: $('input#id_website')
		 */
		validateSingleInput:  function(input_element){
			var data = {[input_element.name]: input_element.value,
				csrfmiddlewaretoken: getCSRF(), };
			var self=this;
			return $.post({
				data: data,
				url: this.url,
				success: function (json_respons){
					self.onFieldError(input_element.name, json_respons);
				},
			});
		},
		/**
		 * check the whole form (all input fields).
		 */
		validateAllInputs: function(){
			var self=this;
			return $.post({
				data: this.getFormData(),
				url: this.url,
				success: function (json_respons){
					var err = 0;
					for(var element_name in json_respons){
						self.onFieldError(element_name, json_respons);
						err++;
					}
					if(err == 0) {
						self.onSuccess();
					}
				},
			});
		},
		setUpTypingValidation: function(){
			var typingTimer; //timer identifier
			var self=this;
			var func_check = function(e){
				clearTimeout(typingTimer);
				typingTimer = setTimeout(function(){
					return self.validateSingleInput(e.target);
				}, self.stop_typing_delay);
			};
			var self = this;
			$(this.selector+" :input").each(function(){
				if($(this).attr("type") != "submit" && $(this).attr("type") != "hidden"){
					$(this).keyup(func_check);
					$(this).keydown(function(){clearTimeout(typingTimer)});
					$(this).focusout(function(e){
						return self.validateSingleInput(e.target);
					});
				}
			});
		},
		setUpFormValidation: function(){
			var self = this;
			$(this.selector+" :submit").click(function(e){
				self.validateAllInputs();
				return false; // avoid to execute the actual form submit
			}); //click
		},
		setItUp: function(){
			if(this.on_typing) {
				this.setUpTypingValidation();
			}
			this.setUpFormValidation();
		},
	}; // AjaxForm
	// only one argument -> use it as options
	if(typeof form_selector === 'object' && typeof url === 'undefined'
		&& typeof options === 'undefined'){
			options = form_selector;
	}
	$.extend(AjaxForm, options);
	AjaxForm.setItUp();
	return AjaxForm
} // setUpAjaxForm
