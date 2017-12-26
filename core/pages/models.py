import re
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django.apps import apps

from content_editor.models import create_plugin_base, Region
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from core.contents import create_content_type
from core.contents import content_register
from core.contents.models import ImageContent
from core.contents.models import RichTextContent
from core.contents.models import ApplicationContent
from core.contents import app_reverse

class PageManager(TreeManager):

    active_filter = dict(
        is_active = True,
    )

    #def __init__(self, *args, **kwargs):
    #    super(PageManager, self).__init__(*args, **kwargs)
    #    self.tree_order = ( self.tree_id_attr, self.left_attr)

    def get_nav_pages(self):
        fil = dict(is_in_nav=True)
        fil.update(self.active_filter)
        return self.filter(**fil)

    def get_active(self):
        qs = self.filter(**self.active_filter)
        return qs

class Page(MPTTModel):

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
                            related_name='children', db_index=True)
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

    @classmethod
    def create_content_type(cls, content_type, **kwargs):
        return create_content_type(cls, content_type, **kwargs)

    def has_app_content(self):
        if content_register.get_app_content(self):
            return True
        else:
            return False

class RichText(RichTextContent):
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
            model_obj = model_type.objects.get(id=obj_id)
            real_url = model_obj.get_absolute_url()
            output = output.replace(link_format % link,
                                    "<a href=\"%s\">" % real_url)
        return mark_safe(output)

Page.create_content_type(RichText)
Page.create_content_type(ImageContent)
Page.create_content_type(ApplicationContent, apps=(('blog.urls',_("Blog")),))
