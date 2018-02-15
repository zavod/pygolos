import steem as stm
from steem.post import Post
from apps.reviews.models import Asset, Review
from django.conf import settings
from bittrex.bittrex import Bittrex
from exchanges.coinapult import Coinapult


class BaseBlockchain(object):
    """
    BaseBlockchain backend, allow to work with golos.io and steemit
    """
    nodes = None
    PRIVATE_POSTING_KEY = None
    PRIVATE_ACTIVE_KEY = None
    author = None

    def init(self, **kwargs):
        self.steem = stm.Steem(nodes=self.nodes, keys=[self.PRIVATE_POSTING_KEY, self.PRIVATE_ACTIVE_KEY])

    def publish_post(self, post):
        self.steem.post(title=post.title, permlink=post.slug, body=post.text, author=self.author, tags=post.tags, self_vote=False)

        post.publish = True
        post.save()

    def get_posts(self):
        reviews = Review.objects.filter(publish=True, complete=False)
        for post in reviews:
            self.get_post(post)

    def get_post(self, post):
        if not post.author or post.author != self.author:
            return
        kwargs = {'author': post.author, 'permlink': post.slug}

        try:
            blockchain_post = Post(post=kwargs, steemd_instance=self.steem)
        except:
            return
        votes = blockchain_post.get('net_votes')  # len(post.get('active_votes'))
        post.votes = votes

        # pending reward
        reward_pending_amount = blockchain_post.get('total_pending_payout_value')
        amount = reward_pending_amount.get('amount')
        asset = reward_pending_amount.get('asset')
        if amount > 0:
            post.reward = amount

        self.set_asset(post, asset)

        # payouts reward
        total_payout_value = blockchain_post.get('total_payout_value')
        amount = total_payout_value.get('amount')
        asset = total_payout_value.get('asset')
        self.set_asset(post, asset)

        if amount > 0:
            post.reward = amount
            post.complete = True

        if not post.reward:
            post.save()
            return

        if post.provider == 'golos':
            # calc BTC
            local_course = self.get_local_course()
            if local_course:
                base_course = local_course.get('base')
                if base_course:
                    gbg_course = float(base_course.split(' ')[0])
                    gbg_golos = post.reward / gbg_course

                    api = Bittrex(settings.BITTREX_KEY, settings.BITTREX_SECRET)
                    btc_cost = api.get_ticker('BTC-GOLOS').get('result').get('Ask')
                    post.btc = btc_cost * gbg_golos

                    # calc RUB reward
                    rub_course = Coinapult().get_current_price(currency='RUB')
                    post.rub = post.btc * float(rub_course)
        else:
            return # TODO set it for steem

        post.save()

    def set_asset(self, post, asset_source):
        if asset_source:
            if Asset.objects.filter(title=asset_source).exists():
                asset = Asset.objects.get(title=asset_source)
            else:
                asset = Asset()
                asset.title = asset_source
                asset.save()
            post.asset = asset

    def get_account(self):
        return self.steem.get_account(self.author)

    def get_balance(self):
        return self.get_account()['sbd_balance']

    def get_local_course(self):
        return self.steem.get_current_median_history_price()

    def fill_post_by_source(self, request):
        token = request.POST.get('token')
        if token != settings.BLOCKCHAIN_PRIVATE_KEY:
            return {'result': 'Wrong credentials'}

        source_id = request.POST.get('source_id')
        slug = request.POST.get('slug')
        title = request.POST.get('title')
        tags = request.POST.get('tags')
        text = request.POST.get('text')
        provider = request.POST.get('provider')
        author = self.author

        if not Review.objects.filter(slug=slug).exists():
            review = Review()
            review.source_id = source_id
            review.title = title
            review.slug = slug
            review.text = text
            review.tags = tags
            review.author = author
            review.provider = provider
            review.save()

            # publish to blockchain
            # self.publish_post(post=review)
            return {'result': 'Success'}
        return {'result': 'False', 'msg': "Review doesn't exists"}




