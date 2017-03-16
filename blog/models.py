import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html, mark_safe
from django.shortcuts import render
from django.template.loader import render_to_string

from content_editor.models import create_plugin_base, Region

from contents.models import AbstractImageContent, AbstractRichTextContent

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


class ImageContent(AbstractImageContent, BlogEntryContent):

    def render(self, request, **kwargs):
        # context = kwargs['context']
        context = { }
        context.update({'image_content': self, })
        # kwargs['context'] = context
        return render_to_string('blog/content/image.html', context=context,
                                request=request)
        return format_html(
        '<figure><img src="{}" alt=""/><figcaption>{}</figcaption></figure>',
        self.image.thumbnail['400x400'].url,
        self.caption,
    )


class RichTextContent(AbstractRichTextContent, BlogEntryContent):
    
    def render(self, request, **kwargs):
        return mark_safe(self.text)
    pass
