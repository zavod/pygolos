from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters
from rest_framework import generics

from apps.providers.golos.backend import GolosBackend
from apps.providers.base.backend import BaseBlockchain
from apps.rest_api.serializers import *
from apps.reviews.models import Review


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    model = Review
    queryset = Review.objects.filter(publish=True)
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)

    def get_queryset(self):
        token = self.request.GET.get('token')
        slug = self.request.GET.get('slug')

        try:

            print(token)
            print(settings.BLOCKCHAIN_TOKEN)

            if token != settings.BLOCKCHAIN_TOKEN:
                print('exit now')
                return []

            # get info from blockchain
            print('start get data from blockchain')
            backend = GolosBackend()
            backend.init()
            backend.get_posts()
            print('finish get data from blockchain')

            queryset = Review.objects.filter(publish=True)
            result_string = 'got count %s' % queryset.count()
            print(result_string)
            return queryset
        except Exception as e:
            print(e)
            return []

@csrf_exempt # TODO do it with csrf
def commit_posts(request):
    if request.method == 'POST':
        author = request.POST.get('author')
        backend = BaseBlockchain()
        backend.author = author

        result = backend.fill_post_by_source(request)
        return JsonResponse(result)






