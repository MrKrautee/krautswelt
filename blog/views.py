from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.utils.html import format_html, mark_safe

from content_editor.contents import contents_for_item
from content_editor.renderer import PluginRenderer

from .models import BlogEntry
from .models import RichTextContent, ImageContent

#class EntryDetailView(DetailView):
#    model = BlogEntry
#
#    def get_context_data(self, **kwargs):
#        obj = kwargs['object']
#        contents = []
#        image_contents = ImageContent.objects.filter(parent=obj)
#        # map(lambda a: contents.append(a), image_contents)
#        for o in image_contents:
#            contents.append(o)
#        context = super(EntryDetailView, self).get_context_data(**kwargs)
#        context['contents'] = contents #image_contents[0]
#        return context
#


renderer = PluginRenderer()
renderer.register(
    RichTextContent,
    lambda plugin: mark_safe(plugin.text),
)
#renderer.register(
#    ImageContent,
#    lambda plugin: format_html(
#        '<figure><img src="{}" alt=""/><figcaption>{}</figcaption></figure>',
#        plugin.image.thumbnail['400x400'].url,
#        plugin.caption,
#    ),
#)
renderer.register( ImageContent, lambda content: content.render())
# <img src="{{ instance.image.thumbnail.400x400 }}" />
# <img src="{{ instance.image.crop.400x400 }}" />



def entry_detail(request, slug):
    entry = get_object_or_404(BlogEntry, slug=slug)
    contents = contents_for_item(entry, [RichTextContent, ImageContent])
    main_contents = contents['main']

    print(contents.render)

    html_contents = { }
    for region in entry.regions:
        html_contents[region.key] = mark_safe('')
        for content in contents[region.key]:
            html = content.render(request)
            html_contents[region.key] += html

    return render(request, 'blog/blogentry_detail.html', {
        'object': entry,
        'contents': html_contents
        # {
        #     #'main': c.render(request) for c in main_contents
        #     'main': c.render(request) for c in contents['main']
        #     # region.key: renderer.render(contents[region.key])
        #     # region.key: (c.render() for c in contents[region.key]) 
        #     # for region in entry.regions
        # },
    })
    return render(request, 'blog/entry.html', {'entry': entry})


def entry_list(request):
    pass

def category_list(request):
    pass

