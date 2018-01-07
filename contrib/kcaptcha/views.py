from django.shortcuts import render
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from .forms import captcha_form_factory

# Create your views here.

def captcha_ajax(request, model_form):
    if request.method == "POST" and request.is_ajax():
        if 'captcha_1' in request.POST.keys():
            CaptchaForm = captcha_form_factory(model_form)
            form_captcha = CaptchaForm(request.POST)
            if form_captcha.is_valid():
                model_form.save()
            else:
                key = CaptchaStore.generate_key()
                url = captcha_image_url(key)
                audio_url = reverse('captcha-audio', args=[key])
                reload_popover_html = render_to_string(
                    'captcha/reload_popover.html',
                                {})
                # need no exact error message but captcha reload.
                # use data structure same as model_form.erros because javascript
                # expecting it... (? dirty or not ?)
                new_captcha = {
                    'captcha_1': {
                        'url': url,
                        'audio_url': audio_url,
                        'key': key,
                        'errors':
                        form_captcha.errors['captcha'],
                        'error_placeholder': _('please try again.'),
                        'reload_popover_html': reload_popover_html,
                    }
                }
                return JsonResponse(new_captcha)
        return JsonResponse(model_form.errors)
    else:
        return HttpResponseNotAllowed(('POST',))

