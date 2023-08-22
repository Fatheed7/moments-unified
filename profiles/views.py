from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from rest_framework import generics,filters
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__following', distinct=True),
        followed_count=Count('owner__followed', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile'
    ]
    ordering_fields = [
        ('posts_count', 'Post Count'),
        ('followers_count', 'Follower Count'),
        ('followed_count', 'Followed Count'),
        ('owner__following__created_at', 'Most Recent Follower'),
        ('owner__followed__created_at', 'Most Recently Followed'),
    ]

class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__following', distinct=True),
        followed_count=Count('owner__followed', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]