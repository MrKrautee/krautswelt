from django.forms import ModelForm
from django.forms import HiddenInput
from django.forms import CharField
from django.utils.safestring import mark_safe

from contrib.forms import KModelForm
from captcha.fields import CaptchaField

class CaptchaModelForm(KModelForm):
    """ Model Form with ajax captcha """

    class Media(KModelForm.Media):
        js = ('kcaptcha/js/captcha_form.js',)

    class Meta(KModelForm.Meta):
        pass

def captcha_form_factory(model_form_cls, hide_model_form=True):
    meta  = model_form_cls.Meta
    hidden_widgets = { }
    if hide_model_form:
        for field_name in meta.fields:
            hidden_widgets.update({field_name: HiddenInput()})
    class PlusCaptchaForm(ModelForm):
        captcha = CaptchaField(required=True)

        class Meta:
            model = meta.model
            fields = meta.fields
            widgets = hidden_widgets
    return PlusCaptchaForm

