# -*- coding: utf-8 -*-
from django import forms
from tinymce.widgets import TinyMCE
from models import *
from django.utils.translation import ugettext_lazy as _


class ReviewForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "", 'class': 'rounded-input', 'name': "tags"}))

    class Meta:
        model = Review
        fields = ['title', 'campaign', 'youtube_link', 'text', 'link', 'subtitle',]
        exclude = ['profile']
        widgets = {'text': forms.Textarea(attrs={'cols': '140', 'rows': '150'}),
                   'title': forms.TextInput(attrs={'placeholder': "", 'class': 'rounded-input', 'name': "header"}),
                   'youtube_link': forms.TextInput(attrs={'placeholder': "", 'class': 'rounded-input', 'name': "youtube"}),
                   'subtitle': forms.Textarea(attrs={'placeholder': "", 'class': 'crw-textarea', 'name': 'subtitle'}),
                   'link': forms.TextInput(attrs={'class': 'rounded-input', 'name': 'link'}),
                   'campaign': forms.Select(attrs={'class': 'rounded-input', 'name': 'campaign'}),
                   }


