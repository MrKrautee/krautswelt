 
$( document ).ready(function() {

  // Comment Form
  //needed for captcha
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

  };
  applyCSS();

  // using jQuery
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
  };
  $('#btn-write-comment').click(function(e){

    var comment_from_div = $("div#comment_form");
    // if no there is an empty div -> add form
    if($.trim(comment_from_div.html()).length == 0){
      $.ajax({
        method: "POST",
        url: "/blog/comment/form/",
        data: { csrfmiddlewaretoken: getCookie('csrftoken'), },
        success: function(response_html) {
          $("div#comment_form").append(response_html);
          applyCSS();
  $('#comment_submit').click(function(e){
    // collect data
    var data = getCommentFormData();
    $.ajax({
      method: "POST",
      url: "/blog/comment/form/",
      data: data,
      success: function(response_html) {
      $("div#comment_form").html(response_html);
        applyCSS();
      },

  });
  return false; // avoid to execute the actual from submit
  }); //click
        },
      }); //ajax
    }else{ // hide form if it already exists
      comment_from_div.hide();
       $("button#btn-write-comment").click(function(){
           $("div#comment_form").toggle();
       });
    };

  });

}); // ready
