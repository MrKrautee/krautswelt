from django.conf.urls import url
from blog.views import entry_detail
from blog.views import entry_archive
from blog.views import comment_form_check
from blog.views import BlogEntryListView
from blog.views import BlogEntryMonthArchive
from blog.views import BlogEntryDayArchive
from blog.views import BlogEntryYearArchive

urlpatterns = [
    url(r'^comment/form/check/$', comment_form_check,
        name='comment_form_check'),
    url(r'^list/$', BlogEntryListView.as_view(),
        name='entry_list'),
    url(r'^archive/$', entry_archive,
        name='entry_archive'),
    url(r'^archive/([0-9]{4})/$', BlogEntryYearArchive.as_view(),
        name='entry_archive_year'),
    url(r'^archive/([0-9]{4})/([0-9]{1,2})/$', BlogEntryMonthArchive.as_view(),
        name='entry_archive_month'),
    url(r'^archive/([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})/$', BlogEntryDayArchive.as_view(),
        name='entry_archive_day'),

    url(r'^(?P<slug>[-\w]+)/$', entry_detail,
        name='entry_detail'),
]
