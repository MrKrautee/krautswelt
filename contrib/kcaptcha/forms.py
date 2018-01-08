from django.forms import ModelForm
from django.forms import HiddenInput
from django.forms import CharField
from django.utils.safestring import mark_safe

from captcha.fields import CaptchaField

class CaptchaModelForm(ModelForm):
    """ Model Form with ajax captcha """
    def ajax_config(self):
        raise NotImplemented

    @property
    def js_data(self, *args, **kwargs):
        ajax_config = self.ajax_config()
        extra_js = "<script type='text/javascript'>var Kcaptcha = { %s };</script>"
        js_data = [
            "url:'%s'," % ajax_config['url'],
            "model_form_selector:'%s form'," % ajax_config['model_form_div_id'],
            "captcha_form_selector:'%s form'," % ajax_config['captcha_form_div_id'],
        ]
        js_output = extra_js % '\n'.join(js_data)
        return mark_safe(js_output)

    class Media:
        js = (
            'kcaptcha/js/captcha_form.js',
            'krautswelt/js/forms.js',
        )

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

