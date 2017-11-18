# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render,redirect
from models import *
from apps.tools.utils import items_paginator
from django.views.generic.detail import DetailView
from django.http import JsonResponse, Http404
from apps.store.models import Category
from .forms import ReviewForm
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def add_tags(review, tags):
    tags = tags.split(',')
    for tag in tags:
        if not ReviewTags.objects.filter(title=tag):
            newtag = ReviewTags(title=tag)
            newtag.save()
            review.tags.add(newtag)
        else:
            tag = ReviewTags.objects.get(title=tag)
            review.tags.add(tag)


def add_link(profile, link, title, campaign):
    custom_link = CustomLink()
    custom_link.url = link
    custom_link.title = title
    custom_link.campaign = campaign
    custom_link.profile = profile
    custom_link.save()

    return custom_link


def add_files(files, review):
    for name_image, image_file in files.iteritems():
        new_image = ReviewImage()
        if name_image == 'cover':
            new_image.cover = True
        new_image.image = image_file
        new_image.review = review
        new_image.save()


def reviews(request, slug_category=None, slug_user=None):
    """review view"""

    context = {}

    context['current_menu'] = 'reviews'
    reviews = Review.objects.filter(publish=True)
    popular_campaigns = Campaign.objects.filter(virtual=False).order_by('-rating')[:5]
    categories = Category.objects.all()
    if slug_category:
        reviews = Review.objects.filter(tags__slug__contains=slug_category)
    if slug_user:
        reviews = Review.objects.filter(profile__id=slug_user)
    reviews = items_paginator(request, reviews)
    context['review_list'] = reviews
    context['popular_campaigns'] = popular_campaigns
    context['categories'] = categories
    template = settings.TEMPLATE_DIR + '/reviews/list.html'

    return render(request, template, context)


@login_required
def add_review(request):
    """This view adds new review"""

    context = {}
    template = settings.TEMPLATE_DIR + '/reviews/add_review.html'
    profile = request.user.user_profile

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        files = request.FILES
        if form.is_valid():
            data = form.cleaned_data
            review_link = data.get('link')
            review_title = data.get('title')

            if not Review.objects.filter(profile=profile, title=review_title):


                review = form.save(commit=False)
                review.profile = request.user.user_profile
                review.datetime = datetime.datetime.now()
                review.save()

                #add images
                if files:
                    add_files(files, review)


                #create short link

                review.custom_link = add_link(profile,review_link,review_title,review.campaign)

                # add tags
                add_tags(review, data.get('tags'))

                review.save()

                result = {'result': True, 'review': review}

                return result
            else:
                form.errors['AlreadyExists'] = "У вас уже есть обзор с таким названием"

        result = {'result': False, 'errors': form.errors}

        return result

    else:
        form = ReviewForm()
        context['form'] = form
        context['back_url'] = request.META.get('HTTP_REFERER')
        return render(request, template, context)


def update_review(request,review,tags):
    """This review updates information in review if user has changed"""

    form = ReviewForm(request.POST, request.FILES, instance=review, initial={'tags': tags})
    if form.is_valid():
        # update base information
        form.save()
        files = request.FILES
        data = form.cleaned_data
        changed_data = form.changed_data
        # update tags
        if 'tags' in changed_data:
            add_tags(review, data.get('tags'))
        # update custom_link
        if ('link' or 'campaign' or 'title') in changed_data:
            profile = request.user.user_proile
            link = data.get('link')
            title = data.get('title')
            campaign = review.campaign
            review.custom_link = add_link(profile, link, title, campaign)
        # update files
        if files:
            add_files(files, review)

        review.save()

        result = {'result': True, 'review': review}

        return result
    else:
        result = {'result': True, 'errors': form.errors}

        return result


@login_required
def review_preview(request, slug):
    """Return page for preview user's review"""
    context = {}

    template = settings.TEMPLATE_DIR + '/reviews/preview.html'
    review = Review.objects.get(slug=slug)
    context['object'] = review

    return render(request, template, context)


@login_required
def review_preview_check(request):
    """If user click 'preview' before 'publish"""
    result = add_review(request)
    if result['result']:
        review = result['review']
        url = review.get_preview_url()

        return JsonResponse({'result': True, 'url': url})
    else:
        return JsonResponse({'result': False, 'errors': result['errors']})


@login_required
def change_review(request, slug):
    """View for page, where user can change review """
    context = {}

    template = settings.TEMPLATE_DIR + '/reviews/add_review.html'
    review = Review.objects.get(slug=slug)
    context['object'] = review

    tags = review.tags.values_list('title', flat=True)
    tags = ",".join(tags)

    if request.method == 'GET':
        cover_image = ReviewImage.objects.get(review=review, cover=True)

        if review.profile == request.user.user_profile:
            form = ReviewForm(instance=review, initial={'tags': tags})
            context['form'] = form
            context['cover_image'] = cover_image
            context['review'] = review
            context['back_url'] = request.META.get('HTTP_REFERER')

            return render(request, template, context)
        else:
            raise Http404
    else:

        result = update_review(request, review, tags)

        if result['result']:

            review = result['review']
            url = review.get_preview_url()

            return JsonResponse({'result': True, 'url': url})
        else:
            return JsonResponse({'result': False, 'error': result['errors']})


@login_required
def publish_review(request):
    """Publish new review, without preview"""
    profile = request.user.user_profile

    result = add_review(request)
    if result['result']:
        review = result['review']
    else:
        return JsonResponse({'result': False, 'errors': result['errors']})

    if profile == review.profile:
        review.publish = True
        review.save()

        url = review.get_full_url()

        return JsonResponse({'result': True, 'url': url})

    else:
        return JsonResponse({'result': False})

def publish_preview(request,slug):
    """Publish review from 'preview' page"""
    profile = request.user.user_profile
    review = Review.objects.get(slug=slug)
    if profile == review.profile:
        review.publish = True
        review.save()

    return redirect('review', slug=slug)


def publish_change(request, slug):
    """Publish review from page where user changes review"""
    review = Review.objects.get(slug=slug)
    profile = request.user.user_profile
    tags = review.tags.values_list('title', flat=True)
    tags = ",".join(tags)
    result = update_review(request, review, tags)

    if result['result']:
        if profile == review.profile:
            review.publish = True
            review.save()

            url = review.get_full_url()

            return JsonResponse({'result': True, 'url': url})
    else:
        return JsonResponse({'result': False, 'error': result['errors']})




class ReviewDetailView(DetailView):
    model = Review

    def get_context_data(self, **kwargs):
        context = super(ReviewDetailView, self).get_context_data(**kwargs)
        review = context['object']
        context['back_url'] = self.request.META.get('HTTP_REFERER')
        if review.visitors == None:
            review.visitors = 1
        else:
            review.visitors += 1
        review.save()


        return context


    def get_template_names(self):
        template_name = settings.TEMPLATE_DIR + '/reviews/review.html'
        return [template_name]


