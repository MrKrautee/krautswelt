from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from content_editor.admin import ContentEditor
from core.contents.admin import create_inlines
from .models import Page

content_inlines = create_inlines(Page)
class PageAdmin(ContentEditor):

    fieldsets = (
        (None, {
            'fields': ('title', 'slug',)
        }),
        (_("publication"), {
            'classes': ('collapse',),
            'fields': ('pub_date', 'is_active', 'create_date')
        }),
        (_("seo"), {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_keywords', 'meta_description'),
        }),
        (_("permissions"), {
            'classes': ('collapse',),
            'fields': (),
        }),
        (_("dev"), {
            'classes': ('collapse',),
            'fields': ('ordering', 'parent'),
        })

    )
    inlines = content_inlines 
    readonly_fields = ('create_date', )
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'is_active', 'ordering', 'parent', 'get_children', 'pub_date')
    list_editable = ('is_active', )

    def get_children(self, obj):
        return list(obj.get_children())
    get_children.short_description=_("children")

admin.site.register(Page, PageAdmin)
