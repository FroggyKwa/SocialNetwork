from django.urls import path

from . import views

urlpatterns = [
    path("post", views.PostUploadView.as_view(), name="upload_post"),
]
