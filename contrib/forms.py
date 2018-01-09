from django.forms import ModelForm
from django.utils.safestring import mark_safe

class KModelForm(ModelForm):
    """ ModelForm with:
        * extra javascript data,
        * Bootstrap form class,
        * ajax functionality
    """

    # name for js object which includes the extra js data from js_config().
    js_form_name = None

    # css class to add to each form field.
    css_field_classes = (
        'form-control', # Bootstrap form class
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #set css classes
        for name, field in self.fields.items():
            old_css_class = field.widget.attrs.get('class', '')
            if len(old_css_class)>0:
                old_css_class +=' '
            css_classes = ' '.join(self.css_field_classes)
            field.widget.attrs['class'] = "%s%s" % (old_css_class, css_classes)

    @property
    def js_config(self):
        """ defines extra js variables to use in *.js files.
            return: dict with key=js variable name, value=js variable value.

            example: return dict( my_js_var = compute.some.foobar() ).
                you can call it in your js-file through 'js_form_name',
                assuming js_form_name = "MyFormWithFoo":
                    MyFormWithFoo.my_js_var

        """
        return dict()

    @property
    def js_data(self):
        """ returns safestring with <script> including the extra js data.
            example output:
                <script>
                var (js_form_name) = {
                    my_js_var: 'value',
                    ajax_url: '/ajax/request/path',
                }</script>
                used in krautswelt/forms/form.html  {{ form.js_data }}

        """
        if len(self.js_config):
            if not self.js_form_name:
                raise NotImplemented("%s: static field 'js_from_name' not defined."
                                    % self.__class__.__name__)
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

