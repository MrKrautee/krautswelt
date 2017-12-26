from django.db import models
from django.urls import resolve

from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django.utils.html import mark_safe
from django.template.loader import render_to_string

from ckeditor.fields import RichTextField
from versatileimagefield.fields import PPOIField, VersatileImageField


class ImageContent(models.Model):

    """
    Image plugin
    """
    image = VersatileImageField(
        _('image'),
        upload_to='images/%Y/%m',
        width_field='width',
        height_field='height',
        ppoi_field='ppoi',
    )
    width = models.PositiveIntegerField(
        _('image width'),
        blank=True,
        null=True,
        editable=False,
    )
    height = models.PositiveIntegerField(
        _('image height'),
        blank=True,
        null=True,
        editable=False,
    )
    ppoi = PPOIField(_('primary point of interest'))
    caption = models.CharField( _('caption'), max_length=200, blank=True)

    IMAGE_ALIGN_CHOICES = (('l', 'left'), ('r', 'right'), ('n', 'none'))
    css_float = models.CharField(_('css float'),
                                 max_length=1,
                                 choices=IMAGE_ALIGN_CHOICES,
                                 default='r')

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return self.image.name

    def render(self, request, **kwargs):
        app_label = self.__class__._meta.app_label
        content_name = str(self.__class__.__name__).lower()
        template = '%s/content/%s/%s.html' % (app_label, self.region,
                                              content_name)
        html = render_to_string(template, request=request,
                                context={'object':self, })
        return mark_safe(html)


class RichTextContent(models.Model):

    text = RichTextField(
        _('text'),
        config_name='richtext-content',
         # CKEDITOR.config.extraPlugins:
         extra_plugins=['internal_links'],

         # CKEDITOR.plugins.addExternal(...)
         external_plugin_resources=[(
             'internal_links',
             '/static/pages/js/ckeditor/plugins/internal_links/',
             'plugin.js',
         )],
    )

    class Meta:
        verbose_name = _('rich text')
        verbose_name_plural = _('rich texts')

    def __str__(self):
        # Return the first few words of the content (with tags stripped)
        return Truncator(strip_tags(self.text)).words(10, truncate=' ...')

    def render(self, *args, **kwargs):
        return mark_safe(self.text)

class ApplicationContent(models.Model):
    @classmethod
    def init(cls, apps = ()):
        choices = [ (k, v) for k, v in apps ]
        cls.add_to_class('urls_conf', models.CharField(max_length=100,
                                                       choices=choices))

    def render(self, request, **kwargs):
        full_path = request.path
        cnt_info = kwargs['content_info']
        page_path = cnt_info.parent.get_absolute_url()
        app_path = full_path.replace(page_path, '')
        fn, args, kwargs = resolve("/%s"%app_path, self.urls_conf)
        #kwargs['extra_context'] =  dict(page = cnt_info.parent)
        return fn(request, *args, **kwargs)


