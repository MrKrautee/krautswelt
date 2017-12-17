from django.conf.urls import url

from .views import page_view


urlpatterns = [

    url(r'^(?P<full_slug>.*)/$', page_view,
        name='page_view'),
]

