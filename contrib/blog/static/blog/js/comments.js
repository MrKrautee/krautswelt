// @require: jQuery
// @require: kcaptcha/js/captcha_form.js

$(document).ready(function() {

  makeBootstrapForms(Kcaptcha.model_form_selector, Kcaptcha.captcha_form_selector);

  // if captcha is valid:
  fadeOutCommentForm = function () {
    // success msg.
    $('div#comments .alert').fadeIn('slow');
    // hide comment form.
    $('div#comments div#comment_form_panel').fadeOut('slow');
  };

  setUpCaptchaForm(
    Kcaptcha.url, // validation (ajax) url
    Kcaptcha.model_form_selector, // model_from
    Kcaptcha.captcha_form_selector, //captcha_form
    fadeOutCommentForm // onSucess
  );

});
