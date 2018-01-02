from django.conf.urls import url
from .views import article_detail
from .views import article_archive
from .views import comment_form_check
from .views import ArticleListView
from .views import ArticleMonthArchive
from .views import ArticleDayArchive
from .views import ArticleYearArchive

urlpatterns = [
    url(r'^comment/form/check/$', comment_form_check,
        name='comment_form_check'),
    url(r'^$', ArticleListView.as_view(),
        name='article_list'),
    url(r'^archive/$', article_archive,
        name='article_archive'),
    url(r'^archive/([0-9]{4})/$', ArticleYearArchive.as_view(),
        name='article_archive_year'),
    url(r'^archive/([0-9]{4})/([0-9]{1,2})/$', ArticleMonthArchive.as_view(),
        name='article_archive_month'),
    url(r'^archive/([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})/$', ArticleDayArchive.as_view(),
        name='article_archive_day'),

    url(r'^(?P<slug>[-\w]+)/$', article_detail,
        name='article_detail'),
]
