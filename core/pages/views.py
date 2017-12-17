from django.shortcuts import render
from django.http.response import Http404

from django.shortcuts import get_object_or_404, get_list_or_404
from core.contents.views import render_content_to_string
from .models import Page
from .models import PageRichTextContent, PageImageContent


def page_view(request, full_slug):
    slugs = full_slug.split('/')
    page = None
    if len(slugs) > 1:
        qs = Page.objects.filter(slug=slugs[-1])
        i = 2
        while not qs and i <= len(slugs):
            qs = Page.objects.filter(slug=slugs[-i])
            i = i + 1
        i = i - 1
        for q in qs:
            matching_path ='/'.join(slugs[0:len(slugs)-i+1])
            if q.get_absolute_url().strip('/') == matching_path:
                page = q
                break
    elif len(slugs) == 1:
        page = get_object_or_404(Page, slug=slugs[0])

    if not page:
        return Http404
    app_contents = page.pages_pageapplicationcontent_set.all()
    if app_contents:
        return app_contents[0].render(request)


    contents = render_content_to_string(request, page,
                                        [PageRichTextContent, PageImageContent])
    template_name = "pages/page.html"
    return render(request, template_name, {
        'page': page,
        'contents': contents,
    })
