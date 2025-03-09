"""
Configuration des URLs principales pour le projet KENGAN.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="KENGAN API",
        default_version='v1',
        description="API pour la plateforme de duels KENGAN",
        terms_of_service="https://www.kengan.com/terms/",
        contact=openapi.Contact(email="support@kengan.com"),
        license=openapi.License(name="Propriétaire"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Documentation API
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Admin Django
    path('admin/', admin.site.urls),
    
    # API authentification
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API applications
    path('api/auth/', include('apps.accounts.urls')),
    path('api/user/', include('apps.accounts.urls_user')),
    path('api/duels/', include('apps.duels.urls')),
    path('api/questions/', include('apps.questions.urls')),
    path('api/wallet/', include('apps.wallet.urls')),
    path('api/community/', include('apps.community.urls')),
    path('api/ranking/', include('apps.ranking.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/admin/', include('apps.admin_dashboard.urls')),
    path('api/demo/', include('apps.core.urls')),
]

# Servir les médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
