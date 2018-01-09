from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed
from django.views import View
from django.shortcuts import render
from django.template.loader import render_to_string

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from .forms import captcha_form_factory

# Create your views here.

class SimpleCaptchaFromView(View):
    popover_template = 'kcaptcha/reload_popover.html'
    model_form_class = None
    get_captcha_key = CaptchaStore.generate_key

    def __init__(self, *args, **kwargs):
        self.model_form_class = kwargs.pop('model_form_class')
        super().__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            model_form = self.model_form_class(request.POST)
            if 'captcha_1' in request.POST.keys():
                captcha_form_class = captcha_form_factory(self.model_form_class)
                form_captcha = captcha_form_class(request.POST)
                if form_captcha.is_valid():
                    model_form.save()
                else:
                    key = self.get_captcha_key()
                    url = captcha_image_url(key)
                    audio_url = reverse('captcha-audio', args=[key])
                    popover_html = render_to_string(self.popover_template, {})
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
                            'reload_popover_html': popover_html,
                        }
                    }
                    return JsonResponse(new_captcha)
            return JsonResponse(model_form.errors, safe=False)
        else:
            return HttpResponseNotAllowed((request.method))

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed((request.method))

