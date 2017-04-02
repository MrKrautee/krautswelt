$( document ).ready(function() {
  var form_selector = "div#comment_form form";
  /**
   * collect form data
   */
  function getCommentFormData(){
    // collect data
    var parent = $(form_selector+' input#id_parent').val();
    var name = $(form_selector+' input#id_name').val();
    var email = $(form_selector+' input#id_email').val();
    var website = $(form_selector+' input#id_website').val();
    var comment = $(form_selector+" textarea#id_comment").val();
    var entry_id = $("#context-data").attr('data');
    var csrftoken = getCookie('csrftoken');
    var data = {
      name: name,
      email: email,
      comment: comment,
      website: website,
      parent: parent,
      csrfmiddlewaretoken: csrftoken,
    }
    return data;
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
        showInputErrors(input_element.name, json_respons);
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
      url: '/blog/comment/form/check/',
      success: function (json_respons){
        var err = 0;
        for(var element_name in json_respons){
          showInputErrors(element_name, json_respons);
          err++;
        }
        if(err == 0) {
          $('.alert').fadeIn('slow');
          $('div#comments div#comment_form_panel').fadeOut('slow');
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
    if ( error ) {
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

  function applyCSS(){
    var func_check = function(e){ return checkInput(e.target);};
    $(form_selector+" :input").each(function(){
      if($(this).attr("type") != "submit" && $(this).attr("type") != "hidden"){
        $(this).keyup(func_check);
        $(this).focusout(func_check);
      }
    });
  } //applyCSS

  function isno_form_error(){
    var err = 0;
    $(form_selector+" .form-errors").each( function (){
      var l = $.trim($(this).html()).length;
      err +=l;
    });
    return !(err>0);
  }

  function setCSSandJS(){
    applyCSS();
    $(form_selector+" :submit").click(function(e){
      // if(isno_form_error()){
        var ajax_deferred = checkAllInput();
        // $.when(ajax_deferred).done(function(r){
        //   if(isno_form_error()){
        //     // maybe call captcha view
        //     var data = getCommentFormData();
        //     return $.post({
        //       // @TODO: call ajax view /blog/comment/form/check/
        //       url: "/blog/comment/form/",
        //       data: data,
        //       success: function(response_html) {
        //         $("div#comment_form").html(response_html);
        //         setCSSandJS(); },
        //     });
        //   }
        // });
      }
      return false; // avoid to execute the actual form submit
    }); //click
  } // setCSSandJS


  /* *** MAIN *** */
  setCSSandJS();


}); // ready
