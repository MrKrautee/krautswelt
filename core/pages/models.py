from django.db import models
from django.utils.translation import ugettext_lazy as _

from content_editor.models import create_plugin_base, Region
from mptt.models import MPTTModel, TreeForeignKey

from core.contents import create_content_type
from core.contents import content_register
from core.contents.models import ImageContent
from core.contents.models import RichTextContent
from core.contents.models import ApplicationContent
from core.contents import app_reverse

class PageManager(models.Manager):
    pass

class Page(MPTTModel):

    title = models.CharField(_('title'), max_length=155)
    slug = models.CharField(_('slug'), max_length=155, unique=True)
    create_date = models.DateTimeField(_('creation date'), auto_now_add=True,
                                       editable=False)
    pub_date = models.DateTimeField(_('publication date'), null=True,
                                    blank=True)
    is_active = models.BooleanField(_('is active'), default=False)

    # Meta
    meta_title = models.CharField(_('meta title'), max_length=255, blank=True)
    meta_description = models.CharField(_('meta description'), max_length=255,
                                       blank=True)
    meta_keywords = models.CharField(_('meta keywords'), max_length=255,
                                     blank=True)


    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    ordering = models.IntegerField(default=0)
    regions = (
        Region(key='main', title=_('Main')),
        Region(key='sidebar', title=_('Sidbar'))
    )

    class MPTTMeta:
        order_insertion_by = ['ordering']

    objects = PageManager()

    def get_absolute_url(self):
        ancestors = self.get_ancestors(include_self=True)
        slug = '/'.join([a.slug for a in ancestors])
        url = "/%s/" % slug
        return url

    def __str__(self):
        return "%s" % self.title

    @classmethod
    def create_content_type(cls, content_type, **kwargs):
        return create_content_type(cls, content_type, **kwargs)

    def has_app_content(self):
        if content_register.get_app_content(self):
            return True
        else:
            return False

Page.create_content_type(RichTextContent)
Page.create_content_type(ImageContent)
Page.create_content_type(ApplicationContent, apps=(('blog.urls',_("Blog")),))
