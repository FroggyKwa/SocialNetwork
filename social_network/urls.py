from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login", views.LoginView.as_view(), name="login_view"),
    path("signup", views.SignUpView.as_view(), name="signup_view"),
    path("post_upload", views.PostUploadView.as_view(), name="upload_post"),
    path("post/<post_id>", views.PostDetailView.as_view(), name="post_detail"),
]
