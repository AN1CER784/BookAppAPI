"""
URL configuration for BookAppAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

from BookAppAPI.custom_router import EnhancedAPIRouter
from BookAppAPI.settings import DEBUG
from catalog.api.routers import router as catalog_router
from library.api.routers import router as library_router
from recommendations.api.routers import router as recommendations_router
from reviews.api.routers import router as reviews_router

router = EnhancedAPIRouter()

router.register('catalog', catalog_router, basename="catalog")
router.register('library', library_router, basename="library")
router.register('feedback', reviews_router, basename="feedback")
router.register('recommendations', recommendations_router, basename="recommendations")

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.authtoken')),
    path('api/v1/drf-auth/', include('rest_framework.urls')),

    path('api/v1/', include(router.urls)),
]

if DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns.extend([path('api/v1/schema', SpectacularAPIView.as_view(), name='schema'),
                        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), ])
