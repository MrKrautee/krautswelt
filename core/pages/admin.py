from functools import partial, reduce, update_wrapper
from django.forms.widgets import Widget, ChoiceFieldRenderer, RadioChoiceInput
from django.forms.widgets import RendererMixin, Select, ChoiceInput
from django.contrib import admin
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django.utils.html import format_html
from django.urls import reverse

from django import forms
from django.template.response import TemplateResponse
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin

from content_editor.admin import ContentEditor
from core.contents.admin import create_inlines
from .models import Page

#content_inlines = create_inlines(Page)
def mk_indented_title(instance):
    box_drawing = []
    ancestors = instance.get_ancestors()
    for i in range(instance.level ):
        if instance.level - 1 == i:
            if instance.get_next_sibling():
                box_drawing.append('<i class="child"></i>')
            else:
                box_drawing.append('<i class="last-child"></i>')
        else:
            if i+1 < len(ancestors) and ancestors[i+1].get_next_sibling():
                box_drawing.append('<i class="transition"></i>')
            else:
                box_drawing.append('<i class="o"></i>')

    return format_html(
        '<div class="box">'
        '<div class="box-drawing">{}</div>'
        '<div class="box-text" style="text-indent:{}px">{}</div>'
        '</div>',
        mark_safe(''.join(box_drawing)),
        ((float(instance.level-1) * 30) + 15),
        instance,
    )

class PageChoiceInput(ChoiceInput):
    input_type = 'radio'
    def render(self, name=None, value=None, attrs=None):
        if self.id_for_label:
            label_for = format_html(' for="{}"', self.id_for_label)
        else:
            label_for = ''
        attrs = dict(self.attrs, **attrs) if attrs else self.attrs
        return format_html(
            '<td>{}</td><td><label{}>{}</label></td>',
            self.tag(attrs), label_for, self.choice_label
        )

class PageChoiceFieldRenderer(ChoiceFieldRenderer):
    choice_input_class = PageChoiceInput
    outer_html = '<table{id_attr}>{content}</table>'
    inner_html = '<tr>{choice_value}{sub_widgets}</tr>'

class PageSelectWidget(RendererMixin, Select):
    renderer = PageChoiceFieldRenderer

class PageMoveForm(forms.Form):
    POSITIONS = (
        ('first-child', _('first child')),
        ('last-child', _('last child')),
        ('left', _('before')),
        ('right', _('after')),
    )
    page_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        PAGE_TREE =[
            (p.id, mk_indented_title(p))
                    for p in Page.objects.all()
        ]
        self.fields['target'] = forms.ChoiceField(widget=PageSelectWidget(),
                                                  choices=PAGE_TREE)
        self.fields['position'] = forms.ChoiceField(
            widget=forms.RadioSelect(),
            choices=PageMoveForm.POSITIONS
        )

def action_activate(modeladmin, request, qs):
    for q in qs:
        q.is_active = True
        q.save()
action_activate.short_description = _("activate")

def action_deactivate(modeladmin, request, qs):
    for q in qs:
        q.is_active = False
        q.save()
action_deactivate.short_description = _("deactivate")

def action_set_navigation(modeladmin, request, qs):
    for q in qs:
        q.is_in_nav = True
        q.save()
action_set_navigation.short_description = _("put in navigation")

def action_del_navigation(modeladmin, request, qs):
    for q in qs:
        q.is_in_nav = False
        q.save()
action_del_navigation.short_description = _("remove in navigation")

class PageAdmin(ContentEditor):

    fieldsets = (
        (None, {
            'fields': ('title', 'slug',)
        }),
        (_("publication"), {
            'classes': ('collapse',),
            'fields': ('pub_date', 'is_active', 'is_in_nav', 'create_date',
                       'overwrite_url')
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
    inlines = create_inlines(Page)
    readonly_fields = ('create_date', )
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        'indented_title',
        'get_links',
        'get_absolute_url',
        'is_in_nav',
        'is_active',
        'level',
        'parent',
        'get_children',
        'pub_date'
    )
    actions = (
        action_activate,
        action_deactivate,
        action_set_navigation,
        action_del_navigation,
    )
    list_editable = ()

    def get_children(self, obj):
        return list(obj.get_children())
    get_children.short_description=_("children")

    def get_links(self, obj):
        info = (
            self.admin_site.name,
            self.model._meta.app_label,
            self.model._meta.model_name
        )
        urls = [
            (
                reverse("%s:%s_%s_move" % info, args=(obj.id,)),
                _('move')
            ),
            (
                "%s?parent=%d" % (reverse("%s:%s_%s_add" % info), obj.id),
                _('+child')
            )
        ]
        url_format = "<a href='%s'>%s</a>"
        urls_html = [ url_format % u for u in urls ]
        return mark_safe(" | ".join(urls_html))
    get_links.short_description=""

    def indented_title(self, instance):
        """
        Use Unicode box-drawing characters to visualize the tree hierarchy.
        """
        return mk_indented_title(instance)
    indented_title.short_description = _('title')

    def move_view(self, request, page_id, extra_context=None):
        opts = self.model._meta
        app_label = opts.app_label
        page = Page.objects.get(id=page_id)
        if request.POST: # form submit
            form = PageMoveForm(data=request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                position = cd['position']
                target_id = cd['target']
                target = Page.objects.get(id=target_id)
                page.move_to(target, position)
                return self.changelist_view(request, extra_context)
        else:
            form = PageMoveForm(initial={'page_id': page_id})
        context = {'form': form,
                   'page': page,
                   'descendants': [ p.id for p in page.get_descendants() ],
                   'opts': opts,
                   'app_label': app_label,}
        return TemplateResponse(request, "admin/%s/%s/move_page.html" %
                                (app_label, opts.model_name), context)

    def get_urls(self):
        s_urls = super(PageAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)
        urlpatterns = [
            url(r'^(.+)/move/$', wrap(self.move_view),
                name="%s_%s_move" % info),
        ]
        urls_merged = urlpatterns + s_urls
        return urls_merged
admin.site.register(Page, PageAdmin)
