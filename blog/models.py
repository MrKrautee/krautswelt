import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from content_editor.models import create_plugin_base, Region

from . import contents

class Category(models.Model):

    name = models.CharField(max_length=100)


class BlogEntryManager(models.Manager):

   def get_queryset(self):
       qs = super(BlogEntryManager, self).get_queryset()
       return qs

   def get_active(self):
       qs = self.get_queryset().filter(is_active=True)
       qs = qs.filter(pub_date__lte=datetime.datetime.now())
       return qs


class BlogEntry(models.Model):

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=100)
    pub_date = models.DateTimeField(_('publication date'))
    create_date = models.DateTimeField(_('creation date'), auto_now_add=True,
                                       editable=False)
    last_change = models.DateTimeField(_('last change date'), auto_now=True,
                                   editable=False)
    is_featured = models.BooleanField(_('is featured'), default=False)
    is_active = models.BooleanField(_('is active'), default=False)


    categories = models.ManyToManyField(Category, verbose_name=_('categories'),
                                                                 related_name='blogentries',
                                                                 blank=True)

    #@TODO: related_entries

    regions = (Region(key='main', title=_('Main')), )

    objects = BlogEntryManager()

BlogEntryContent = create_plugin_base(BlogEntry)


class ImageContent(contents.ImageContent, BlogEntryContent):
    pass


class RichTextContent(contents.RichTextContent, BlogEntryContent):
    pass
