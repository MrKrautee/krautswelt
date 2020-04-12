from django.db import models
from django.utils import timezone
from django.db.utils import IntegrityError
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

class Template(models.Model):
    path = models.CharField(_('path'), max_length=255, unique=True)
    name = models.CharField(_('name'), max_length=100, unique=True)
    regions = models.CharField(_('regions'), max_length=255)

    def __str__(self):
        return "%s (%d)" % (self.name, len(self.regions.split(',')))

class PageManager(TreeManager):

    active_filter = dict(
        is_active = True,
        pub_date__lte = timezone.now(),
    )
    def get_navigation(self):
        fil = dict(is_in_nav=True)
        fil.update(self.active_filter)
        return self.filter(**fil)
    get_nav_pages = get_navigation

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
    template = models.ForeignKey(Template, null=True, blank=True,
                                 on_delete=models.CASCADE)

    class MPTTMeta:
        pass

    class Meta:
        unique_together = ('parent', 'slug')

    objects = PageManager()

    # @classmethod
    # def register_templates(cls, templates):
    #     """ templates =[
    #             ('path/to/templ.html', 'My 2-col temlplate', ('main', 'sidebar')),
    #             ('path/to/another/templ.html', 'My 4-col temlplate', ('main',)),
    #         ]
    #     """


    #     # check if regions existing
    #     template_regions = set([ region for path, name, regions in templates for
    #                            region in regions ])
    #     page_regions = [ region.key for region in cls.regions ]
    #     for t_region in template_regions:
    #         try:
    #             page_regions.index(t_region)
    #         except ValueError as e:
    #             msg = "%s does not exist in %s. " + \
    #                          "Only templates with regions existing in " + \
    #                         "%s can be added."
    #             raise Exception(msg % (t_region, cls.__name__, cls.__name__))



    def get_absolute_url(self):
        if self.overwrite_url:
            return self.overwrite_url
        ancestors = self.get_ancestors(include_self=True)
        slug = '/'.join([a.slug for a in ancestors])
        url = "/%s/" % slug
        return url

    def __str__(self):
        return "%s" % self.title

templates = [
    ('base.html', '2 - cols Base', ('main', 'sidebar')),
    ('2base.html', '3 - cols Base', ('main', 'sidebar', )),
    ('4base.html', '4- cols Base', ('main',  )),
]
# @TODO: 
for path, name, regions in templates:
    try:
        Template.objects.create(path=path, name=name,
                                        regions=','.join(regions))
    except IntegrityError as e:
        pass

Page.create_content_type(RichTextContent)
Page.create_content_type(ImageContent)
Page.create_content_type(ApplicationContent, apps=[('contrib.blog.urls',_("Blog")),])
