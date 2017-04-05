from django.conf.urls import url
from blog.views import entry_detail, comment_form_check

urlpatterns = [
    url(r'^comment/form/check/', comment_form_check,
        name='comment_form_check'),
    url(r'^(?P<slug>[-\w]+)/$', entry_detail,
        name='entry-detail'),
]
