from django.urls import URLPattern, path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from blog.api.views import PostViewSet, UserDetail, UserList, TagViewSet



router = routers.DefaultRouter()
#register your ViewSets here
# router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('token-auth/', obtain_auth_token),
    path('jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/<str:email>/', UserDetail.as_view(), name='api_user_detail'),
    path('users/', UserList.as_view(), name='api_user_list')
]

urlpatterns += router.urls

