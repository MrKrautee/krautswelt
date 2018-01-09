import re
from django.db import models
from django.urls import resolve
from django.apps import apps

from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django.utils.html import mark_safe
from django.template.loader import render_to_string

from core.contents import create_content_type
from core.contents import content_register

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
    )

    class Meta:
        verbose_name = _('rich text')
        verbose_name_plural = _('rich texts')

    def __str__(self):
        # Return the first few words of the content (with tags stripped)
        return self.excerpt(word_count=10)

    def excerpt(self, word_count=200):
        no_tags = strip_tags(self.text)
        return Truncator(no_tags).words(word_count, truncate=' ...')


    def render(self, *args, **kwargs):
        link_format = "<a href=\"kwelt://%s/%s/%s/\">"
        regex = link_format % ("(.*?)","(.*?)","(\d+)") + ".*?</a>"
        pattern = re.compile(regex)
        links = re.findall(pattern, self.text)
        output = self.text
        for link in links:
            app_label, model_name, obj_id = link
            model_type = apps.get_model(app_label=app_label,
                                      model_name=model_name)
            try:
                model_obj = model_type.objects.get(id=obj_id)
                real_url = model_obj.get_absolute_url()
            except model_type.DoesNotExist as e:
                # @TODO: 
                real_url = '/404/'
            output = output.replace(link_format % link,
                                    "<a href=\"%s\">" % real_url)
        return mark_safe(output)

class ApplicationContent(models.Model):
    @classmethod
    def init(cls, apps = ()):
        # choices = [ (k, v) for k, v in apps ]
        choices = apps
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


class WithContents(models.Model):
    class Meta:
        abstract = True

    def get_absolute_url(self):
        raise NotImplementedError("%s: needs a get_absolute_url method" %
                                  self.__class__.__name__)

    @classmethod
    def create_content_type(cls, content_type, **kwargs):
        return create_content_type(cls, content_type, **kwargs)

    def getAppContent(self):
        return content_register.get_app_content(self)

    def getContents(self, content_type=None):
        return content_register.get_contents(self, content_type=content_type)

    def getContentTypes(self):
        return content_register.get_ctypes(model_cls=self.__class__)

    def getFirstImage(self):
        return self._getFirst(ImageContent)

    def getFirstRichText(self):
        return self._getFirst(RichTextContent)

    def _getFirst(self, content_type):
        contents = content_register.get_contents(self,
                                                     content_type=content_type)
        if contents.count():
            return contents[0]
        return None


