from rest_framework import permissions, viewsets, generics
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.response import Response

from blog.api.serializers import PostDetailSerializer, TagSerializer, PostSerializer, UserSerializer, UserDetailSerializer
from blango_auth.models import User
from blog.models import Post, Tag
from .permissions import IsAdminUserForObject, AuthorModifyPostOrReadOnly

import logging

logger = logging.getLogger(__name__)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'email'
    serializer_class = UserDetailSerializer
    

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
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



class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited
    """
    queryset = Tag.objects.all().order_by('value')
    serializer_class = TagSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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

