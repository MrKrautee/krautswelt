from django.db import models
from django.utils.translation import ugettext_lazy as _

from content_editor.models import create_plugin_base, Region
from mptt.models import MPTTModel, TreeForeignKey

from core.contents import create_content_type
from core.contents.models import ImageContent
from core.contents.models import RichTextContent
from core.contents.models import ApplicationContent

class PageManager(models.Manager):
    pass

class Page(MPTTModel):

    title = models.CharField(_('title'), max_length=155)
    slug = models.CharField(_('slug'), max_length=155)
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



PageRichTextContent=Page.create_content_type(RichTextContent)
PageImageContent=Page.create_content_type(ImageContent)
PageApplicationContent = Page.create_content_type(
    ApplicationContent, apps=(('blog.urls',_("Blog")),)
                                                 )



#PageContent = create_plugin_base(Page)
#
#class ImageContent(AbstractImageContent, PageContent):
#
#    LEFT = 'l'
#    RIGHT = 'r'
#    NONE = 'n'
#
#    IMAGE_ALIGN_CHOICES = ((LEFT, 'left'), (RIGHT, 'right'), (NONE, 'none'))
#
#    css_float = models.CharField(_('css float'),
#                                 max_length=1,
#                                 choices=IMAGE_ALIGN_CHOICES,
#                                 default=RIGHT)
#
#
#class RichTextContent(AbstractRichTextContent, PageContent):
#
#    def as_str(self):
#        return mark_safe(strip_tags(self.text))
#
#class ApplictionContent(PageContent):
#    # @TODO
#    pass
#
