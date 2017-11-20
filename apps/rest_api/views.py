from rest_framework import routers, serializers, viewsets, generics
from apps.rest_api.serializers import *
from rest_framework import filters
from apps.reviews.models import Review
from django.views.decorators.csrf import csrf_exempt
from apps.golos.backend import GolosBackend
from django.http import JsonResponse

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
            print('got count %s' % queryset.coun())
            return queryset
        except:
            return []

@csrf_exempt # TODO do it with csrf
def commit_posts(request):
    if request.method == 'POST':
        backend = GolosBackend()
        result = backend.fill_post_by_source(request)
        return JsonResponse(result)






