from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import News
from .serializer import NewsSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound





# Viewset for News Model
@csrf_exempt
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    # Action to handle like increment
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        news = self.get_object()
        news.like += 1
        news.save()
        return Response({'status': 'like added', 'like_count': news.like})

    # Action to handle dislike increment
    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        news = self.get_object()
        news.dislike += 1
        news.save()
        return Response({'status': 'dislike added', 'dislike_count': news.dislike})

    # Custom method to fetch a news article with details
    @action(detail=False, methods=['get'])
    def fetch_news(self, request):
        tags = request.query_params.get('tags', None)
        if tags:
            news = News.objects.filter(tags__contains=tags)
        else:
            news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)
    
    # Custom method to update a specific news article
    @action(detail=True, methods=['put'])
    def update_news(self, request, pk=None):
        news = self.get_object()
        serializer = NewsSerializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom method to delete a specific news article
    @action(detail=True, methods=['delete'])
    def delete_news(self, request, pk=None):
        news = self.get_object()
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    @action(detail=True, methods=['get'])
    
    # Get single news
    def get_single_news(self, request, pk=None):
        try:
            news = News.objects.get(pk=pk)
            serializer = NewsSerializer(news)
            return Response(serializer.data)
        except News.DoesNotExist:
            raise NotFound(detail="News item not found.")