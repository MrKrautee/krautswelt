from django.shortcuts import render
from django.shortcuts import get_object_or_404
# from django.views.generic.detail import DetailView
from django.utils.html import mark_safe

# from content_editor.contents import contents_for_item
# from content_editor.renderer import PluginRenderer
from contents.views import render_content_to_string

from .models import BlogEntry
from .models import RichTextContent, ImageContent


def entry_detail(request, slug):
    entry = get_object_or_404(BlogEntry, slug=slug)
    contents = render_content_to_string(request, entry, [RichTextContent, ImageContent])
    return render(request, 'blog/blogentry_detail.html', {
        'object': entry,
        'contents': contents
    })


def entry_list(request):
    pass


def category_list(request):
    pass
