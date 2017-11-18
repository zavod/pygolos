from django.conf.urls import url
from apps.reviews.views import *

urlpatterns = [
    url(r'^reviews/$', reviews, name='reviews_list'),
    url(r'^reviews/add/$', add_review,  name='addreview'),
    url(r'^reviews/category/(?P<slug_category>.*)/$', reviews, name='reviews_category'),
    url(r'^reviews/user/(?P<slug_user>.*)/$', reviews, name='reviews_user'),
    url(r'^reviews/preview/new/$', review_preview_check, name='reviews_preview_check'),
    url(r'^reviews/preview/(?P<slug>.*)/$', review_preview, name='reveiw_preview'),
    url(r'^reviews/publish/new/$', publish_review, name='reveiw_publish_new_review'),
    url(r'^reviews/publish/preview/(?P<slug>.*)/$', publish_preview, name='reveiw_publish_preview'),
    url(r'^reviews/publish/change/(?P<slug>.*)/$', publish_change, name='reveiw_publish_change'),
    url(r'^reviews/change/(?P<slug>.*)/$', change_review, name='reveiw_change'),
    url(r'^reviews/(?P<slug>.*)/$', ReviewDetailView.as_view(), name='review'),
]