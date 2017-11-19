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
            if token != settings.API_TOKEN:
                return []

            # get info from blockchain
            backend = GolosBackend()
            backend.init()
            backend.get_posts()

            queryset = Review.objects.filter(publish=True)
            return queryset
        except:
            return []

@csrf_exempt # TODO do it with csrf
def commit_posts(request):
    if request.method == 'POST':
        backend = GolosBackend()
        result = backend.fill_post_by_source(request)
        return JsonResponse(result)






