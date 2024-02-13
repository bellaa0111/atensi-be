"""bem_psiko_be URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from rest_framework import routers
from main.viewset import *

router = routers.DefaultRouter()
router.register('penilaian', PenilaianViewSet)
router.register('pertanyaan', PertanyaanViewSet)
router.register('upload', FileUploadViewSet, basename='upload')
router.register('integrateSheet', IntegrateSheet, basename='integrate')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('user/', UserViewSet.as_view({'post': 'user_detail'}) ),
    path('chaining/', include('smart_selects.urls')),
]
