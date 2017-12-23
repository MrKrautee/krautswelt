from .models import Page

def navigation(request):
    nav_dict = [
        { 'title': p.title, 'url': p.get_absolute_url() }
        for p in Page.objects.get_nav_pages()
    ]
    return { 'navigation': nav_dict }

