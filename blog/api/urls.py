from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from blog.api.views import PostViewSet, UserViewSet


router = routers.DefaultRouter()
#register your ViewSets here
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)