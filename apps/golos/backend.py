import steem as stm
from steem.post import Post
from apps.reviews.models import Asset, Review
from django.conf import settings
GOLOS_NODES = ['https://ws.golos.io', ]

### TEST ###
test_user = 'cyberfounder'
test_wif = '5JVFFWRLwz6JoP9kguuRFfytToGU6cLgBVTL9t6NB3D3BQLbUBS'
GOLOS_TEST_NODES = ['46.101.132.158:2004', '6.101.132.158:8096']
GOLOS_TEST_MODE = False
test_url = 'http://testnet3.golos.io'

# Big post
test_blog_user = 'rusteemitblog'
test_blog_post = 'kuratorskie-voznagrazhdeniya-i-stimulirovanie-golosovaniya-daniel-larimer'
from bittrex.bittrex import Bittrex
from exchanges.coinapult import Coinapult

class GolosBackend(object):
    def init(self, **kwargs):
        if GOLOS_TEST_MODE:
            pass
            # self.steem = stm.Steem(nodes=GOLOS_TEST_NODES, keys=[PRIVATE_POSTING_KEY, ACTIVE_KEY])
        else:
            self.steem = stm.Steem(nodes=GOLOS_NODES, keys=[settings.PRIVATE_POSTING_KEY, settings.ACTIVE_KEY])

    def get_posts(self):
        pass

    def publish_post(self, post):
        golos_post = self.steem.post(title=post.title, permlink=post.slug, body=post.text, author=settings.GOLOS_USER,
                          tags=['kubish', 'кэшбэк', 'cashbacks', 'покупки',], self_vote=True)

        post.publish = True
        post.save()

    def get_post(self, post):
        asset_source = None
        kwargs = {'author': post.golos_user, 'permlink': post.slug}
        golos_post = Post(post=kwargs, steemd_instance=self.steem)
        votes = golos_post.get('net_votes') # len(post.get('active_votes'))
        post.votes = votes


        # pending reward
        reward_pending_amount = golos_post.get('total_pending_payout_value')
        amount = reward_pending_amount.get('amount')
        asset = reward_pending_amount.get('asset')
        if amount > 0:
            post.reward = amount

        self.set_asset(post, asset)

        # payouts reward
        total_payout_value = golos_post.get('total_payout_value')
        amount = total_payout_value.get('amount')
        asset = total_payout_value.get('asset')
        self.set_asset(post, asset)
        if amount > 0:
            post.reward = amount
            post.complete = True

        # calc BTC
        gbg_course = float(self.get_local_course().get('base').split(' ')[0])
        gbg_golos = post.reward / gbg_course

        api = Bittrex(settings.BITTREX_KEY, settings.BITTREX_SECRET)
        btc_cost = api.get_ticker('BTC-GOLOS').get('result').get('Ask')
        post.btc = btc_cost * gbg_golos

        # calc RUB reward
        rub_course = Coinapult().get_current_price(currency='RUB')
        post.rub = post.btc * float(rub_course)

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
        return self.steem.get_account(settings.GOLOS_USER)

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
        text = request.POST.get('text')
        golos_user = settings.GOLOS_USER

        if not Review.objects.filter(slug=slug).exists():
            review = Review()
            review.source_id = source_id
            review.title = title
            review.slug = slug
            review.text = text
            review.golos_user = golos_user
            review.save()

            # publish to blockchain
            # self.publish_post(post=review)
            return {'result': 'Success'}
        return {'result': 'False', 'msg': "Review doesn't exists"}




