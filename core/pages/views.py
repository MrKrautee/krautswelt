from django.http.response import Http404
from django.shortcuts import get_object_or_404

from core.contents.views import render_content

from .models import Page

def _dissolve(request, slugs, parent=None):
    try:
        page = get_object_or_404(Page, slug=slugs[0], parent=parent)
        if len(slugs) > 1:
            for ch in page.get_children():
                ch_page = get_object_or_404(Page, slug=slugs[1], parent=page)
                slugs_new = slugs[2:]
                if slugs_new:
                    return _dissolve(request, slugs_new, parent=ch_page)
                else:
                    return ch_page
        return page
    except Http404 as e:
        return None

def page_view(request, full_slug):
    slugs = full_slug.split('/')
    page = _dissolve(request, slugs)
    if not page:
        raise Http404("no match for %s" % full_slug)
    if not page.has_app_content():
        if page.get_absolute_url().strip('/') != full_slug.strip('/'):
            raise Http404("no match for %s" % full_slug)
    return render_content(page, request, template_name="pages/page.html")

