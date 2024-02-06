from django.urls import URLPattern, path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from blog.api.views import PostViewSet, UserDetail, UserList, TagViewSet



router = routers.DefaultRouter()

#swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Blango API",
      default_version='v1',
      description="API for Blog",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   url=f"https://127.0.0.1:8000/api/v1/",
   public=True
)

#register your ViewSets here
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)

# generic views urls
urlpatterns = [
    path('users/<str:email>/', UserDetail.as_view(), name='api_user_detail'),
    path('users/', UserList.as_view(), name='api_user_list'),
    path("posts/by-time/<str:period_name>/", PostViewSet.as_view({"get": "list"}), name="posts-by-time"),
]

urlpatterns = format_suffix_patterns(urlpatterns)

#swagger urls
urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

#auth urls
urlpatterns += [
    path('token-auth/', obtain_auth_token),
    path('jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

#viewset urls
urlpatterns += router.urls

