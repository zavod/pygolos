# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.conf import settings
from apps.reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('source_id', 'slug', 'votes', 'rub', )