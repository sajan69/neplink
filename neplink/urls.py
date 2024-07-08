"""
URL configuration for neplink project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, FriendshipViewSet
from posts.views import PostViewSet, LikeViewSet, CommentViewSet
from chat.views import ChatMessageViewSet, CallLogViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Create a router and register viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'friendships', FriendshipViewSet)
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'chat_messages', ChatMessageViewSet)
router.register(r'call_logs', CallLogViewSet)

# Swagger schema view
schema_view = get_schema_view(
   openapi.Info(
      title="Neplink API",
      default_version='v1',
      description="API documentation for Neplink",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@neplink.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('accounts/', include('allauth.urls')),  # For authentication
]

# Add static and media URLs in development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

