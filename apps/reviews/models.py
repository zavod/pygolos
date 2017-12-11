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

PROVIDERS = (
    ('golos', 'golos'),
    ('steem', 'steem'),
)

class Review(models.Model):
    source_id = models.IntegerField('source id', blank=True, null=True)
    provider = models.CharField('provider', max_length=255, choices=PROVIDERS, default='golos')
    author = models.CharField('author', max_length=255, blank=True, null=True)
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
    tags = models.CharField('tags', max_length=255, blank=True, null=True, help_text="only 5 tags")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/review/%s/' % self.slug

    def get_out_link(self):
        if self.provider == 'golos':
            return 'https://golos.io/@%s/%s/' % (self.author, self.slug)
        # TODO set for steem

    def get_full_url(self):
        path = settings.HOST + self.get_absolute_url()
        return path





