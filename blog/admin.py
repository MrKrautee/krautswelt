from django.contrib.admin import ModelAdmin, site
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from content_editor.admin import ContentEditor

from contents.admin import create_inline

from .models import ImageContent, RichTextContent
from .models import BlogEntry, Category, Comment

ImageInline = create_inline(model=ImageContent)
RichTextInline = create_inline(model=RichTextContent)


class CategoryAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', )
    search_fields = ('name', 'slug', )
    ordering = ('name', 'slug', )


class BlogEntryAdmin(ContentEditor):

    inlines = [ImageInline, RichTextInline, ]
    readonly_fields = ('create_date', )
    list_display = ('title', 'pub_date', 'create_date')
    prepopulated_fields = {"slug": ("title",)}
    # fields =
    # fielfsets =
    view_on_site = True
    search_fields = ('title', )
    list_filter = ('pub_date', 'create_date')
    ordering = ('title', 'pub_date', 'create_date')

    def view_on_site(self, obj):
        url = reverse('entry-detail', kwargs={'slug': obj.slug})
        return url


# in case that krautswelt is installed.
# indicate new comments to approve, in admin index.
try:
    from krautswelt.admin import admin_site

    def msg_new_comment(request):
        comments_qs = Comment.objects.get_unapproved()
        comments_count = comments_qs.count()
        msg = _('%i new comment(s) to approve.') % comments_count
        url = '/test/url/to/voew/'
        if comments_count > 0:
            return {'msg': msg, 'url': url}
        return None
    admin_site.register_notification(Comment, msg_new_comment)
except:
    pass

site.register(Category, CategoryAdmin)
site.register(BlogEntry, BlogEntryAdmin)
