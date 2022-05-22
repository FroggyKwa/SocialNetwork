from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login", views.LoginView.as_view(), name="login_view"),
    path("signup", views.SignUpView.as_view(), name="signup_view"),
    path("post_upload", views.PostUploadView.as_view(), name="upload_post"),
    path("post/<post_id>", login_required(views.PostDetailView.as_view(), "redirect_to", login_url="login_view"),
         name="post_detail"),
    path(
        "users/<username>", login_required(views.UserSearchView.as_view(), "redirect_to", login_url="login_view"),
        name="users_search"
    ),
    path("user/<username>", login_required(views.ProfilePageView.as_view(), "redirect_to", login_url="login_view"),
         name="profile_page"),
    path("/profile_update", login_required(views.ProfileUpdateView.as_view(), "redirect_to", login_url="login_view"),
         name="profile_update"),
]
