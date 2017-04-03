function makeAjaxValidationForm(form_selector, url, func_data, func_onSuccess, validate_on_key, func_onError){  
  var form_selector = form_selector;
  var validation_url = url;
  var getCommentFormData = func_data;
  var onSuccess = func_onSuccess;
  if (typeof validate_on_key === 'undefined') { validate_on_key = true; }
  if (typeof func_onError === 'undefined') { func_onError = showInputErrors; }
  /** 
   * check a singel input field.
   * @input_element (dom element) ie: $('input#id_website')
   */
  function checkInput(input_element){
    var data = {[input_element.name]: input_element.value,
      csrfmiddlewaretoken: getCSRF(), };
    return $.post({
      data: data,
      url: validation_url,
      success: function (json_respons){
        func_onError(input_element.name, json_respons);
      },
    });
  }
  /**
   * check the whole form (all input field).
   */
  function checkAllInput(){
    var data = getCommentFormData();
    return $.post({
      data: data,
      url: validation_url,
      success: function (json_respons){
        var err = 0;
        for(var element_name in json_respons){
          func_onError(element_name, json_respons);
          err++;
        }
        if(err == 0) {
          onSuccess();
        }
      },
    });
  }
  /**
   * adds/ removes errors to html error div.
   * @param: {DOM el} input_element ie: $('input#id_email').
   * @param: {json} json_response ajax response with field errors.
   */
  function showInputErrors(element_name, json_response){
    // var element_name = input_element.name;
    var error = json_response[element_name];
    if(error){
      $(form_selector+" #"+element_name+"_help").hide();
      $(form_selector+" #"+element_name+"_errors").html(error);
      $(form_selector+" #id_"+element_name).parent().addClass("has-error");;
      $(form_selector+" #id_"+element_name).next().addClass("glyphicon-remove");
    }else{
      $(form_selector+" #"+element_name+"_help").show();
      $(form_selector+" #"+element_name+"_errors").html("");
      $(form_selector+" #id_"+element_name).parent().removeClass("has-error");
      $(form_selector+" #id_"+element_name).parent().addClass("has-success");
      $(form_selector+" #id_"+element_name).next().removeClass("glyphicon-remove");
      $(form_selector+" #id_"+element_name).next().addClass("glyphicon-ok");
    }
  }
  /* *** MAIN *** */
  if(validate_on_key){
    var func_check = function(e){ return checkInput(e.target);};
    $(form_selector+" :input").each(function(){
      if($(this).attr("type") != "submit" && $(this).attr("type") != "hidden"){
        $(this).keyup(func_check);
        $(this).focusout(func_check);
      }
    });
  }
  $(form_selector+" :submit").click(function(e){
    checkAllInput();
    return false; // avoid to execute the actual form submit
  }); //click

}
