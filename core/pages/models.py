from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe

from content_editor.models import create_plugin_base, Region
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from core.contents.models import ImageContent
from core.contents.models import RichTextContent
from core.contents.models import ApplicationContent
from core.contents.models import WithContents
from core.contents import app_reverse

class PageManager(TreeManager):

    active_filter = dict(
        is_active = True,
        pub_date__lte = timezone.now(),
    )

    def get_nav_pages(self):
        fil = dict(is_in_nav=True)
        fil.update(self.active_filter)
        return self.filter(**fil)

    def get_active(self):
        qs = self.filter(**self.active_filter)
        return qs

class Page(MPTTModel, WithContents):

    title = models.CharField(_('title'), max_length=155)
    slug = models.CharField(_('slug'), max_length=155)
    create_date = models.DateTimeField(_('creation date'), auto_now_add=True,
                                       editable=False)
    pub_date = models.DateTimeField(_('publication date'), null=True,
                                    blank=True)
    is_active = models.BooleanField(_('is active'), default=False)
    is_in_nav = models.BooleanField(_('is in navigation'), default=False)
    overwrite_url = models.CharField(_('overwrite url'), max_length=255,
                                     blank=True, null=True)

    # Meta / SEO
    meta_title = models.CharField(_('meta title'), max_length=255, blank=True)
    meta_description = models.CharField(_('meta description'), max_length=255,
                                       blank=True)
    meta_keywords = models.CharField(_('meta keywords'), max_length=255,
                                     blank=True)


    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True,
                            on_delete=models.CASCADE)
    ordering = models.IntegerField(default=0)
    regions = (
        Region(key='main', title=_('Main')),
        Region(key='sidebar', title=_('Sidbar'))
    )

    class MPTTMeta:
        pass

    class Meta:
        unique_together = ('parent', 'slug')

    objects = PageManager()

    def get_absolute_url(self):
        if self.overwrite_url:
            return self.overwrite_url
        ancestors = self.get_ancestors(include_self=True)
        slug = '/'.join([a.slug for a in ancestors])
        url = "/%s/" % slug
        return url

    def __str__(self):
        return "%s" % self.title


Page.create_content_type(RichTextContent)
Page.create_content_type(ImageContent)
Page.create_content_type(ApplicationContent, apps=(('contrib.blog.urls',_("Blog")),))
