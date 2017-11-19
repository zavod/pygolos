from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from apps.rest_api.urls import urlpatterns as api_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

]

urlpatterns += api_urls