
from apps.providers.golos.backend import GolosBackend
from apps.providers.steem.backend import SteemBackend

class BaseProvider(object):
    def get_review_provider(self, review):
        def get_blockchain_provider(self):
            backend = None
            if review.provider == 'golos':
                backend = GolosBackend()
            elif review.provider == 'steem':
                backend = SteemBackend()
            return backend