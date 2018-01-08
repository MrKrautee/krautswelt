// @require: jQuery
// @require: kcaptcha/js/captcha_form.js

$(document).ready(function() {
  // if captcha is valid:
  fadeOutCommentForm = function () {
    // success msg.
    $('div#comments .alert').fadeIn('slow');
    // hide comment form.
    $('div#comments div#comment_form_panel').fadeOut('slow');
  };
  setUpCaptchaForm(
    CommentKCaptcha.url, // validation (ajax) url
    CommentKCaptcha.model_form_selector, // model_from
    CommentKCaptcha.captcha_form_selector, //captcha_form
    fadeOutCommentForm // onSucess
  );
});

