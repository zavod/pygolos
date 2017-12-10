from django.db import models
from django.utils import timezone

from django.conf import settings


class Asset(models.Model):
    title = models.CharField('title', max_length=255)

    def __str__(self):
        return self.title

REVIEW_STATUSES = (
    ('pending', 'pending'),
    ('payout', 'payout'),
)


class Review(models.Model):
    source_id = models.IntegerField('source id', blank=True, null=True)
    golos_user = models.CharField('golos user', max_length=255, blank=True, null=True)
    title = models.CharField('title', max_length=1000)
    slug = models.SlugField('slug', blank=True, null=True, max_length=1000)
    text = models.TextField('text')
    votes = models.IntegerField('votes', default=0)
    reward = models.FloatField('reward', blank=True, null=True)
    btc = models.FloatField('BTC', blank=True, null=True)
    rub = models.FloatField('RUB', blank=True, null=True)
    asset = models.ForeignKey(Asset, related_name='asset_reviews', blank=True, null=True)
    status = models.CharField('status', max_length=255, choices=REVIEW_STATUSES, blank=True, null=True)
    publish = models.BooleanField('publish', default=False)
    complete = models.BooleanField('complete', default=False)
    tags = models.CharField('tags', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/review/%s/' % self.slug

    def get_out_link(self):
        return 'https://golos.io/@%s/%s/' % (self.golos_user, self.slug)

    def get_full_url(self):
        path = settings.HOST + self.get_absolute_url()
        return path

    def get_preview_url(self):
        path = settings.CAB_HOST + '/review/preview/%s/' % self.slug
        return path

    def get_preview_check_url(self):
        path = settings.CAB_HOST + '/review/preview/check/%s/' % self.slug
        return path

    def get_publish_change_url(self):
        path = settings.CAB_HOST + '/review/publish/change/%s/' % self.slug
        return path

    def get_change_url(self):
        path = settings.CAB_HOST + '/review/change/%s/' % self.slug
        return path

    def get_publish_preview_url(self):
        path = settings.CAB_HOST + '/review/publish/preview/%s/' % self.slug
        return path

    def get_image(self):
        if self.review_images.count() > 0:
            if self.review_images.filter(cover=True).exists():
                return self.review_images.filter(cover=True)[0]
            else:
                return self.review_images.all()[0]

    def get_approve_cashback(self):
        custom_link = self.custom_link.id
        cashback = self.profile.get_approve_cashback_queryset().filter(order__history__item=custom_link)
        if cashback:
            return cashback[0].rate
        else:
            return 0

    def get_waiting_cashback(self):
        custom_link = self.custom_link.id
        cashback = self.profile.get_waiting_cashback_queryset().filter(order__history__item=custom_link)

        if cashback:
            return cashback[0].rate
        else:
            return 0

    def get_paid_cashback(self):
        custom_link = self.custom_link.id
        if self.profile.get_paid_cashback_queryset().filter(order__history__item=custom_link).exists():
            cashback = self.profile.get_paid_cashback_queryset().get(order__history__item=custom_link)

            return cashback[0].rate
        else:
            return 0

    def get_cashback_count(self):
        custom_link = self.custom_link.id
        if self.profile.profile_cashbacks.filter(order__history__item=custom_link).exists():
            count = self.profile.profile_cashbacks.filter(order__history__item=custom_link).count()
            return count
        else:
            return 0


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, related_name='review_images')
    image = models.ImageField('image', upload_to='review')
    cover = models.BooleanField('cover', default=False)

    def __unicode__(self):
        return self.review.title

    def get_full_url(self):
        return '%s%s' % (settings.HOST, self.image.url)

