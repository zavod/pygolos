from django.conf import settings
from apps.providers.base.backend import BaseBlockchain

class GolosBackend(BaseBlockchain):

    def init(self, **kwargs):
        self.nodes = settings.GOLOS_NODES
        self.PRIVATE_POSTING_KEY = settings.GOLOS_PRIVATE_POSTING_KEY
        self.PRIVATE_ACTIVE_KEY = settings.GOLOS_PRIVATE_ACTIVE_KEY
        self.author = settings.GOLOS_USER
        super(GolosBackend, self).init() # TODO check it





