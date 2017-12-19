from django.shortcuts import render
from django.http.response import Http404

from django.shortcuts import get_object_or_404, get_list_or_404
#from core.contents.views import render_content_to_string
from core.contents.views import render_content
from .models import Page



def _disolve(request, slugs):
    try:
        page = get_object_or_404(Page, slug=slugs[0])
        if len(slugs) > 1:
            for ch in page.get_children():
                ch_page = get_object_or_404(Page=slugs[1], parent=page)
                slugs_new = slugs[2:]
                return _disolve(request, slugs_new)
        return page
    except Http404 as e:
        return None


def page_view(request, full_slug):
    slugs = full_slug.split('/')
    page = _disolve(request, slugs)
    print("page> %s" % str(page))
    # page = None
    # if len(slugs) > 1:
    #     qs = Page.objects.filter(slug=slugs[-1])
    #     i = 2
    #     while not qs and i <= len(slugs):
    #         qs = Page.objects.filter(slug=slugs[-i])
    #         i = i + 1
    #     i = i - 1
    #     for q in qs:
    #         matching_path ='/'.join(slugs[0:len(slugs)-i+1])
    #         if q.get_absolute_url().strip('/') == matching_path:
    #             page = q
    #             break
    # elif len(slugs) == 1:
    #     page = get_object_or_404(Page, slug=slugs[0])

    if not page:
        raise Http404("no match for %s" % full_slug)
    if not page.has_app_content():
        if page.get_absolute_url().strip('/') != full_slug.strip('/'):
            raise Http404("no match for %s" % full_slug)
    return render_content(page, request, template_name="pages/page.html")
