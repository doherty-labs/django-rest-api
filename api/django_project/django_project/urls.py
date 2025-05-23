"""django_project URL Configuration

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
from django.urls import path

from rest_framework import permissions
from rest_framework.schemas import get_schema_view

from rest_api.channels import TaskProgressConsumer
from rest_api.views.sample import SampleViewTest

rest_api_urlpatterns = [
    # Test
    path("sample/get", SampleViewTest.as_view()),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "openapi",
        get_schema_view(
            title="REST API",
            description="API for all things …",
            version="1.0.0",
            permission_classes=[permissions.AllowAny],
            public=True,
            patterns=rest_api_urlpatterns,
        ),
    ),
    *rest_api_urlpatterns,
]

websocket_urlpatterns = [
    path("task/progress/<str:taskID>/", TaskProgressConsumer.as_asgi()),
]
