from django.http.response import Http404
from django.shortcuts import get_object_or_404

from core.contents.views import render_content

from .models import Page

def _dissolve(request, slugs, parent=None):
    """ find (best) match for slugs """
    page = None
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
        if page:
            return page
    return None

class Http404Error(Http404):
    def __init__(self, full_slug):
        self.message = "no match for %s" % full_slug

def page_view(request, full_slug='/'):
    slugs = full_slug.split('/')
    try:
        if len(full_slug)>1:
            full_slug = "/%s/" % full_slug
        # not working for pages with app content
        page = get_object_or_404(Page, overwrite_url=full_slug)
    except Http404 as e:
        page = _dissolve(request, slugs)
    if not page:
        raise Http404Error(full_slug)
    app_ct = page.getAppContent()
    if not app_ct:
        if page.get_absolute_url().strip('/') != full_slug.strip('/'):
            raise Http404Error(full_slug)
    return render_content(page, request, template_name="pages/page.html")

