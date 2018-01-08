from django.forms import ModelForm
from django.utils.safestring import mark_safe

class KModelForm(ModelForm):
    """ ModelForm with bootstrap css class(form-control) for fields """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
           css_class = field.widget.attrs.get('class', '')
           field.widget.attrs['class'] = "%s %s" % ('form-control', css_class)

    @property
    def js_config(self):
        raise NotImplemented

    @property
    def js_data(self):
        extra_js = "<script type='text/javascript'>var %s = { %s };</script>"
        js_data = []
        for name, value in self.js_config.items():
            js_data.append("%s:'%s'," % (name, value))
        js_output = extra_js % (self.js_form_name, '\n'.join(js_data))
        return mark_safe(js_output)

    class Meta:
        pass

    class Media:
        js = ('krautswelt/js/forms.js',)

