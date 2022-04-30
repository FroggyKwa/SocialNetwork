from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("social_network.urls")),
    path("admin/", admin.site.urls),
]
