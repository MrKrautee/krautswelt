from functools import partial
from functools import update_wrapper
from functools import reduce

from django.contrib import admin
from django.conf.urls import url
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.forms.widgets import  RadioSelect
from django.forms.widgets import HiddenInput
from django.forms import ChoiceField
from django.forms import IntegerField
from django.forms import Form

from content_editor.admin import ContentEditor

from core.contents.admin import create_inlines
from core.contents.views import render_content

from .models import Page

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

class PageRadioSelect(RadioSelect):
    template_name = 'pages/forms/widgets/page_radio.html'
    option_template_name = 'pages/forms/widgets/page_radio_option.html'

class PageMoveForm(Form):
    POSITIONS = (
        ('first-child', _('first child')),
        ('last-child', _('last child')),
        ('left', _('before')),
        ('right', _('after')),
    )
    page_id = IntegerField(widget=HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        PAGE_TREE =[
            (p.id, mk_indented_title(p))
                    for p in Page.objects.all()
        ]
        self.fields['target'] = ChoiceField(widget=PageRadioSelect(),
                                                  choices=PAGE_TREE)
        self.fields['position'] = ChoiceField(
            widget=RadioSelect(),
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
            'classes': ('',),
            'fields': ('pub_date', ('is_active', 'is_in_nav'), 'create_date',
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
    raw_id_fields = ('parent', )
    search_fields = ('title', )
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
    save_as = save_on_top = True

    class Media:
        css = dict(
            all=('/static/pages/css/page_tree.css',)
        )
        js = ('/static/admin/contents/js/RelatedLinksLookup.js',)

    def change_form_tools(self, obj_id):
        info = (
            self.admin_site.name,
            self.model._meta.app_label,
            self.model._meta.model_name
        )
        links = (
            (_('Add Child'),
                "%s?parent=%s" % (reverse("%s:%s_%s_add" % info), obj_id)),
            (_('Preview'),
                reverse("%s:%s_%s_preview" % info, args=obj_id)),
            (_('Move'), reverse("%s:%s_%s_move" % info, args=(obj_id,))),
        )
        return links



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
            (reverse("%s:%s_%s_move" % info, args=(obj.id,)),
                _('Move')),
            ("%s?parent=%d" % (reverse("%s:%s_%s_add" % info), obj.id),
                _('+Child')),
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
        page = self.model.objects.get(id=page_id)
        if request.POST: # form submit
            form = PageMoveForm(data=request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                position = cd['position']
                target_id = cd['target']
                target = self.model.objects.get(id=target_id)
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

    def preview_view(self, request, page_id):
        page = self.model.objects.get(id=page_id)
        return render_content(page, request)


    def changeform_view(self, request, object_id=None, form_url='',
                        extra_context=None):
        extra = None
        if object_id:
            extra = dict(object_tools = self.change_form_tools(object_id))
        return super().changeform_view(request, object_id, form_url,
                                               extra_context=extra)

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
            url(r'^(.+)/preview/$', wrap(self.preview_view),
                name="%s_%s_preview" % info),
        ]
        urls_merged = urlpatterns + s_urls
        return urls_merged
admin.site.register(Page, PageAdmin)

