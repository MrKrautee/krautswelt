"""green_life URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf import settings
from django.conf.urls import include, url

from django.conf.urls.static import static

from django.conf.urls import url
from django.contrib import admin

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from blog.views import  entry_detail, comment_form_check
import captcha

media_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static_urls = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = [
    url(r'^blog/comment/form/check/', comment_form_check, name='comment_form_check'),
    url(r'^blog/(?P<slug>[-\w]+)/$', entry_detail,
        name='entry-detail'),
     url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', admin.site.urls),
]

urlpatterns +=media_urls
urlpatterns +=static_urls
# urlpatterns +=staticfiles_urlpatterns()

#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns = [
#        url(r'^__debug__/', include(debug_toolbar.urls)),
#    ] + urlpatterns
