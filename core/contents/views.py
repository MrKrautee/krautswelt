from django.utils.html import mark_safe
from django.shortcuts import render
from django.template.loader import render_to_string

from content_editor.contents import contents_for_item
from . import content_register


def render_content_to_string(request, parent_object, contents_cls_list=None):
    contents = content_register.get_contents(parent_object)
    html_contents = {}
    contents_reg = {}

    #for region in parent_object.regions:
    for content in contents:
        if content.region not in html_contents.keys():
            html_contents[content.region] = mark_safe('')
        if content.region in [ r.key for r in parent_object.regions]:
            html = content.render(request)
            html_contents[content.region] += html
    return html_contents

def render_content(model, request, template_name=None):
    app_content = content_register.get_app_content(model)
    return app_content.render(request)

    contents = render_content_to_string(request, model)
    return render(request, template_name, {
        'model': model,
        'contents': contents,
    })

#def render(self, request, **kwargs):
#    # context = kwargs['context']
#    context = { }
#    context.update({'image_content': self, })
#    # kwargs['context'] = context
#    return render_to_string('blog/content/image.html',
#                            context=context, request=request
#                            )# request=request
#    return format_html(
#    '<figure><img src="{}" alt=""/><figcaption>{}</figcaption></figure>',
#    self.image.thumbnail['400x400'].url,
#    self.caption,
#)
