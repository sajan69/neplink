
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from chat.views import ChatMessageViewSet, CallLogViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static


# Create a router and register viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet)

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
    path('', include('posts.urls'),name='home'),
    path('chat/', include('chat.urls'),name='chat'),
    path('users/', include('users.urls'),name='users'), 
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# add at the last
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
