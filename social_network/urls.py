from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post", views.PostUploadView.as_view(), name="upload_post"),
]
