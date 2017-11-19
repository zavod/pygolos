from rest_framework import routers, serializers, viewsets
from django.conf.urls import include, url
from apps.rest_api.views import *

router = routers.DefaultRouter()

urlpatterns = [
    url('^api/v.0.1/golos/posts/', ReviewList.as_view(), name='rest_api_reviews'),
    url('^api/v.0.1/golos/commit_reviews/', commit_posts, name='rest_api_commit_reviews'),
]
