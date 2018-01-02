from django.contrib.admin import ModelAdmin, site
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django.urls import reverse

from content_editor.admin import ContentEditor
from core.contents.admin import create_inlines

from .models import Article, Category, Comment

blog_content_inlines = create_inlines(Article)
class CategoryAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', )
    search_fields = ('name', 'slug', )
    ordering = ('name', 'slug', )


class ArticleAdmin(ContentEditor):

    inlines = blog_content_inlines # [ImageInline, RichTextInline, ]
    readonly_fields = ('create_date', )
    list_display = ('title', 'pub_date', 'create_date', 'slug', 'is_active')
    prepopulated_fields = {"slug": ("title",)}
    # fields =
    # fielfsets =
    view_on_site = True
    search_fields = ('title', 'pub_date')
    list_filter = ('pub_date', 'create_date', 'is_active')
    ordering = ('title', 'pub_date', 'create_date')
    filter_horizontal = ('related_entries', )

    def view_on_site(self, obj):
        return obj.get_absolute_url()

def approve_comment(modeladmin, request, queryset):
        for comment in queryset:
            comment.approve()
approve_comment.short_description = _("approve comment(s)")
class CommentAdmin(ModelAdmin):
    list_filter = ('is_active', )
    list_display = ('name', 'email', 'comment_excerpt', 'website', 'date', )
    actions = ( approve_comment, )
    readonly_fields = ('comment', 'name', 'email', 'website', 'date',
                       'notify_new_entry', 'notify_new_comment', 'parent_link')

    fieldsets = (
        (None, {
            'fields': ('is_active', 'parent_link'),
        }),
        (_("Comment"), {
            'fields': ('date', 'name', 'email', 'website', 'comment'),
        }),
        (None, {
            'fields': ('notify_new_entry', 'notify_new_comment'),
        }),
    )

    def parent_link(self, obj):
        # @TODO: article preview
        parent = obj.parent
        return mark_safe('<a href="%s">%s</a> (id: %s)' % (parent.get_absolute_url(),
                                                 parent.title, parent.id))
    parent_link.short_description=_('article')
# in case that krautswelt is installed.
# indicate new comments to approve, in admin index.
try:
    from advanced_admin.admin import admin_site

    def msg_new_comment(request):
        comments_qs = Comment.objects.get_unapproved()
        comments_count = comments_qs.count()
        msg = _('%i new comment(s) to approve.') % comments_count
        app_label = Comment._meta.app_label
        model_name = Comment._meta.model_name
        url = reverse('admin:%s_%s_changelist' % (app_label, model_name))
        url = '%s?is_active__exact=0' % url
        if comments_count > 0:
            return {'msg': msg, 'url': url}
        return None
    admin_site.register_notification(Comment, msg_new_comment)
except:
    print("Cant register Comment Notification")
    pass

site.register(Category, CategoryAdmin)
site.register(Article, ArticleAdmin)
site.register(Comment, CommentAdmin)
