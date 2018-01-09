from django import template
from django.utils.html import mark_safe
from ..models import PageManager

register = template.Library()

@register.inclusion_tag('pages/sub_pages_navigation.html', takes_context=False)
def full_sub_navigation(current_page):
    root = current_page.get_root()
    if not root.get_children().filter(**PageManager.active_filter):
        return dict(sub_pages = [], sub_pages_html = '')
    full_tree = root.get_descendants(include_self=True)
    full_tree = full_tree.filter(**PageManager.active_filter)
    html = "<ul>"
    li_link = "<li><a href='%s'>%s</a></li>"
    bold = "<b>%s</b>"
    level = 0
    for page in full_tree:
        if level < page.level:
            html += "<ul>"
        elif level > page.level:
            html += "</ul>"
        if page == current_page:
            title = bold % page.title
        else:
            title = page.title
        html += li_link % (page.get_absolute_url(), title)
        level = page.level
    html += "</ul>"
    return dict(sub_pages_html = mark_safe(html), sub_pages = full_tree)


