
from django.conf.urls import include, url
from advanced_admin.admin import admin_site

urlpatterns = [
    url('', admin_site.urls),
]

