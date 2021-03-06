// @REQUIRE: JqUERY
// @require: bootstrap (CSS)
// @require: /krautswelt/js/forms.js
function setUpCaptchaForm(url, form_selector, captcha_form_selector, onSuccess){
    var CaptchaForm = {
      selector: captcha_form_selector,
      url: url,
      on_typing: false,
      onSuccess: function(){
        // captcha form valid!
        // show notification. and remove commentform 
        onSuccess();
        // $('div#comments div#comment_form_panel').fadeOut('slow');
      },
      onFieldError: function (element_name, json_response){
        // do it for the captcha input only and not for
        // the other fields
        if(element_name === "captcha_1"){
          var captcha_input_selector = this.selector+" input#id_captcha_1";
          var captcha_input = $(captcha_input_selector);
          // reload captcha
          $(this.selector+" img.captcha").attr('src',
            json_response.captcha_1.url);
          $(this.selector+" a#captcha_audio_url").attr('audio-url',
            json_response.captcha_1.audio_url);
          $(this.selector+" input#id_captcha_0").attr('value',
            json_response.captcha_1.key);
          // reset input - show error
          captcha_input.val('');
          captcha_input.next('span.glyphicon').addClass('glyphicon-remove');
          captcha_input.parent().addClass('has-error');
          captcha_input.attr('placeholder', json_response.captcha_1.error_placeholder);
          $(this.selector+' div#id_captcha_help').hide();
          $(this.selector+' div#id_captcha_errors').html(json_response.captcha_1.errors);
          captcha_input.focus();
          // indicate reload with popover
          $(captcha_form_selector+" img.captcha").popover({
            placement: 'right',
            trigger: 'manual',
            html: true,
            animation: true,
            delay: {show: 100, hide: 1500},
            content: json_response.captcha_1.reload_popover_html,
          });
          $(this.selector+" img.captcha").popover('show');
          var self = this;
          setTimeout(function(){
            $(self.selector+" .popover").fadeOut('slow');
            $(self.selector+
              " img.captcha").popover('hide');
          }, 733);
        }
      }
    };
    var CommentForm = {
      selector: form_selector,
      captcha_selector: CaptchaForm.selector,
      url: url,
      onSuccess: function (){
        // model_form is valid!
        // load captcha
        var form_div_select = this.selector.replace(' form', '')
        $(form_div_select).fadeOut();
        // copy comment form data to captcha form
        var self = this;
        $(this.selector+" :input").each(function(){
          if($(this).attr("type") != "submit"){
            var select_new = self.captcha_selector+" #"+$(this).attr('id');
            var val_old = $(this).val();
            $(select_new).val(val_old);
          }
        });
        var captcha_form_div_select = captcha_form_selector.replace(' form', '')
        $(captcha_form_div_select).fadeIn();
      }
    };

    CommentForm = setUpAjaxForm(CommentForm);
    CaptchaForm = setUpAjaxForm(CaptchaForm);
}

function initKCaptchaForm(onSuccess){
  setUpCaptchaForm(
    KCaptcha.url,
    KCaptcha.model_form_selector,
    KCaptcha.captcha_form_selector,
    onSuccess
  );
}
