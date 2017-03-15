from django.db import models

from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags

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

    class Meta:
        abstract = True
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return self.image.name


class RichTextContent(models.Model):

    text = RichTextField(_('text'), config_name='richtext-content')

    class Meta:
        abstract = True
        verbose_name = _('rich text')
        verbose_name_plural = _('rich texts')

    def __str__(self):
        # Return the first few words of the content (with tags stripped)
        return Truncator(strip_tags(self.text)).words(10, truncate=' ...')
