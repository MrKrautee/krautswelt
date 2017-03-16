from django.contrib import admin
from django.urls import reverse

from content_editor.admin import ContentEditor

from contents.admin import create_inline

from .models import ImageContent, RichTextContent
from .models import BlogEntry, Category

ImageInline = create_inline(model=ImageContent)
RichTextInline = create_inline(model=RichTextContent)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', )
    search_fields = ('name', 'slug', )
    ordering = ('name', 'slug', )



class BlogEntryAdmin(ContentEditor):

    inlines = [ ImageInline, RichTextInline, ]
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







admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogEntry, BlogEntryAdmin)
