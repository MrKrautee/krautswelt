from django.forms import ModelForm
from django.forms import HiddenInput

from captcha.fields import CaptchaField

def captcha_form_factory(model_form_cls, hide_model_form=True):
    meta  = model_form_cls._meta
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

