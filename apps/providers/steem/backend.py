from django.conf import settings
from apps.providers.base.backend import BaseBlockchain

class SteemBackend(BaseBlockchain):

    def init(self, **kwargs):
        self.nodes = settings.STEEM_NODES
        self.PRIVATE_POSTING_KEY = settings.STEEM_PRIVATE_POSTING_KEY
        self.PRIVATE_ACTIVE_KEY = settings.STEEM_PRIVATE_ACTIVE_KEY
        self.author = settings.STEEM_USER
        super(SteemBackend, self).init() # TODO check it





