from django.db.models import Count
from rest_framework import permissions, filters
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile'
    ]
    ordering_fields = [
        ('comments_count', 'Comment Count'),
        ('likes_count', 'Like Count'),
        ('likes__created_at', 'Most Recent Like'),
    ]
    search_fields = [
        'owner__username', 'title'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')
