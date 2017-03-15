from django.contrib import admin

from content_editor.admin import ContentEditor, ContentEditorInline

from .models import ImageContent, RichTextContent
from .models import BlogEntry

ImageInline = ContentEditorInline.create(model=ImageContent)
RichTextInline = ContentEditorInline.create(model=RichTextContent)


class BlogEntryAdmin(ContentEditor):

    inlines = [ ImageInline, RichTextInline]
    readonly_fields = ('create_date', 'last_change')
    list_display = ('title', 'pub_date', 'create_date')
    prepopulated_fields = {"slug": ("title",)}
    # fields =
    # fielfsets =
    search_fields = ('title', )
    list_filter = ('pub_date', 'create_date')
    ordering = ('title', 'pub_date', 'create_date')

admin.site.register(BlogEntry, BlogEntryAdmin)
