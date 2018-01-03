from django.http.response import Http404
from django.shortcuts import get_object_or_404

from core.contents.views import render_content

from .models import Page
from .models import PageManager

def _dissolve(slugs, parent=None):
    """ find (best) match page for slugs.
        ie: /path/to/page/some/extra/shit/foo/
        returns page with abs_url: /path/to/page/.

        Args:
            slugs (list of strings): list of slugs, [ 'path', 'to', 'page'].
            parent (Page): parent Page.

        Returns:
            Page: best matching Page Object. None for no match found.
    """
    page = None
    try:
        page = get_object_or_404(Page, slug=slugs[0], parent=parent,
                                 **PageManager.active_filter)
        if len(slugs) > 1:
            for ch in page.get_children():
                ch_page = get_object_or_404(Page, slug=slugs[1], parent=page,
                                            **PageManager.active_filter)
                slugs_new = slugs[2:]
                if slugs_new:
                    return _dissolve(slugs_new, parent=ch_page)
                else:
                    return ch_page
        return page
    except Http404 as e:
        if page:
            return page
    return None

class Http404Error(Http404):
    def __init__(self, full_slug):
        self.message = "No matching Page for %s found!" % full_slug

def page_view(request, full_slug='/'):
    """ matches full_slug to page and renders it """
    slugs = full_slug.split('/')
    try:
        # pages with overwrite_url set
        if len(full_slug)>1:
            full_slug = "/%s/" % full_slug
        # @TODO: ?? not working for pages with app content
        page = get_object_or_404(Page, overwrite_url=full_slug,
                                 **PageManager.active_filter)
    except Http404 as e:
        # best (page) match for full_slug
        page = _dissolve(slugs)
    if not page:
        # no page matching
        raise Http404Error(full_slug)
    app_ct = page.getAppContent()
    if not app_ct:
        # only for AppContents additional subpathes allowed.
        # ie.: /path/to/page_with_app/additional/sub/app/path/
        # for pages without AppContent the full_slug has to match:
        if page.get_absolute_url().strip('/') != full_slug.strip('/'):
            raise Http404Error(full_slug)
    return render_content(page, request, template_name="pages/page.html")

