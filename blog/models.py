import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html, mark_safe
from django.shortcuts import render
from django.template.loader import render_to_string

from content_editor.models import create_plugin_base, Region

from contents.models import AbstractImageContent, AbstractRichTextContent

from comments.models import create_comment_class

class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)

    def __str__(self):
        return self.name


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
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    pub_date = models.DateTimeField(_('publication date'))
    create_date = models.DateTimeField(_('creation date'), auto_now_add=True,
                                       editable=False)
    # last_change = models.DateTimeField(_('last change date'), auto_now=True,
    #                                editable=False)
    is_featured = models.BooleanField(_('is featured'), default=False)
    is_active = models.BooleanField(_('is active'), default=False)


    categories = models.ManyToManyField(Category, verbose_name=_('categories'),
                                                                 related_name='blogentries',
                                                                 blank=True)

    #@TODO: related_entries

    regions = (Region(key='main', title=_('Main')), )

    objects = BlogEntryManager()

    def excerpt(self):
        # @TODO:
        pass

BlogEntryContent = create_plugin_base(BlogEntry)


class ImageContent(AbstractImageContent, BlogEntryContent):

    LEFT='l'
    RIGHT = 'r'
    NONE = 'n'

    IMAGE_ALIGN_CHOICES = ((LEFT, 'left'), (RIGHT, 'right'), (NONE, 'none'))

    css_float = models.CharField(_('css float'), max_length=1,
                             choices=IMAGE_ALIGN_CHOICES, default=RIGHT)


class RichTextContent(AbstractRichTextContent, BlogEntryContent):
    pass

AbstractBlogEntryComment = create_comment_class(BlogEntry)

class EntryComment(AbstractBlogEntryComment):
    pass


