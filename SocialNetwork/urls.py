from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = (
    [
        path("", include("social_network.urls")),
        path("api/", include("api.urls")),
        path("admin/", admin.site.urls),
    ]
    + staticfiles_urlpatterns()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
