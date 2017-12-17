from django.utils.html import mark_safe
from django.shortcuts import render
from django.template.loader import render_to_string

from content_editor.contents import contents_for_item
from . import content_register
from . import mk_ctype_name
from . import mk_related_ctype_name


def render_content_to_string(request, parent_object, contents_cls_list=None):
    contents_cls_list = contents_cls_list or content_register.get_ctypes(parent_object.__class__)
    contents = contents_for_item(parent_object, contents_cls_list)
    html_contents = {}
    for region in parent_object.regions:
        html_contents[region.key] = mark_safe('')
        for content in contents[region.key]:
            # render content
            app_label = content.__class__._meta.app_label
            content_name = str(content.__class__.__name__).lower()
            template = '%s/content/%s/%s.html' % (app_label, region.key,
                                                  content_name)
            html = render_to_string(template, request=request,
                                    context={'object':content, })
            # html = content.render(request)
            html_contents[region.key] += mark_safe(html)
    print(html_contents)
    return html_contents

def render_content(model, request, template_name=None):
    from .models import ApplicationContent
    app_cnt_name = mk_ctype_name(model.__class__, ApplicationContent)
    if app_cnt_name in content_register.get_ctype_names(model.__class__):
        app_cnt_related = mk_related_ctype_name(model.__class__, ApplicationContent)
        app_content = model.__getattribute__(app_cnt_related).all()[0]
        return app_content.render(request)

    contents = render_content_to_string(request, model)
    return render(request, template_name, {
        'model': model,
        'contents': contents,
    })

def render(self, request, **kwargs):
    # context = kwargs['context']
    context = { }
    context.update({'image_content': self, })
    # kwargs['context'] = context
    return render_to_string('blog/content/image.html',
                            context=context, request=request
                            )# request=request
    return format_html(
    '<figure><img src="{}" alt=""/><figcaption>{}</figcaption></figure>',
    self.image.thumbnail['400x400'].url,
    self.caption,
)
