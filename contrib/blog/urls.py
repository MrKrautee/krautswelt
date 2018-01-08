from django.conf.urls import url
from .views import article_archive
from .views import ArticleListView
from .views import ArticleMonthArchive
from .views import ArticleDayArchive
from .views import ArticleYearArchive
from .views import ArticleDetail
from .views import CommentForm
from contrib.kcaptcha.views import SimpleCaptchaFromView

urlpatterns = [
    url(r'^comment/form/check/$',
        SimpleCaptchaFromView.as_view(model_form_class=CommentForm),
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

    url(r'^(?P<slug>[-\w]+)/$', ArticleDetail.as_view(),
        name='article_detail'),
]
