"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework_simplejwt.views import TokenRefreshView

from bzsdp.app.api.controller.member.auth.v1_token_refresh_controller import V1TokenRefreshController
from bzsdp.project.config import BZSDPConfig
urlpatterns = [

    path('api/v2/', include('bzsdp.app.api.dispatcher.dispatcher')),

    path('api/v2/auth/refresh/', V1TokenRefreshController.as_view(), name='token_refresh'),
    path('api/v2/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('django_prometheus.urls')),
]

if BZSDPConfig.is_debug():
    urlpatterns += [path('api/admin/', admin.site.urls), ]

    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

    urlpatterns += [
        # YOUR PATTERNS
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        # Optional UI:
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
