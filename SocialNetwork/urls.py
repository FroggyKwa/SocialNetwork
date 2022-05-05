from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", include("social_network.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()