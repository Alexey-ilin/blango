import time
from django.http import Http404
from rest_framework import permissions, viewsets, generics
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q

from datetime import timedelta

from blog.api.serializers import PostDetailSerializer, TagSerializer, PostSerializer, UserSerializer, UserDetailSerializer
from blango_auth.models import User
from blog.models import Post, Tag
from .permissions import IsAdminUserForObject, AuthorModifyPostOrReadOnly

import logging

logger = logging.getLogger(__name__)

class UserList(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows user with specified email to be viewed
    """
    queryset = User.objects.all()
    lookup_field = 'email'
    serializer_class = UserDetailSerializer
    

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited
    """
    queryset = Post.objects.all().order_by('published_at')
    permission_classes = [AuthorModifyPostOrReadOnly|IsAdminUserForObject]

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return PostSerializer
        return PostDetailSerializer
    
    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        return super().perform_create(serializer)

    #customizing queryset for user
    def get_queryset(self):
        if self.request.user.is_anonymous:
            #only published posts
            queryset = self.queryset.filter(published_at__lte=timezone.now())
        elif self.request.user.is_staff:
            #all posts
            queryset = self.queryset
        else:
            #unpublished + author unpublished posts
            queryset = self.queryset.filter(Q(published_at__lte=timezone.now())|Q(author = self.request.user))
        logger.info(self.args)
        logger.info(self.kwargs)
        logger.info(self.request.headers)
        time_period_name = self.kwargs.get('period_name')
        if not time_period_name:
            return queryset
        match time_period_name:
            case "new":
                return queryset.filter(published_at__gte=timezone.now()-timedelta(hours=1))
            case "day":
                return queryset.filter(published_at__gte=timezone.now()-timedelta(days=1))
            case "week":
                return queryset.filter(published_at__gte=timezone.now()-timedelta(weeks=1))
            case _:
                raise Http404(f"Time period {time_period_name} is now valid, should be "
            f"'new', 'today' or 'week'")



class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited
    """
    queryset = Tag.objects.all().order_by('value')
    serializer_class = TagSerializer

    @method_decorator(cache_page(60*5))
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        tag = self.get_object()
        post_data = tag.posts.all().order_by('-created_at')
        page = self.paginate_queryset(post_data)
        if page is not None:
            post_serializer = PostSerializer(page, many=True, context={"request":request})
            return self.get_paginated_response(post_serializer.data)
        post_serializer = PostSerializer(post_data, many=True, context={"request":request})
        return Response(post_serializer.data)
        

    @method_decorator(cache_page(60*5))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @method_decorator(cache_page(60*5))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

