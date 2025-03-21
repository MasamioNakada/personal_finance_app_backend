"""
URL configuration for personal_finance_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración del esquema de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation Personal finance",  # Título de la API
        default_version='v1',       # Versión por defecto
        description="Descripción de la API",  # Descripción general
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="nakada2130@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,  # Permite acces   o público
    permission_classes=(permissions.AllowAny,),  # Permisos para acceder a la documentación
)

urlpatterns = [
    # Rutas de Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Rutas de la aplicación
    path("admin/", admin.site.urls),
    path('api/', include('api.urls')),
    path('chatbot/', include('chatbot.urls')),
]
