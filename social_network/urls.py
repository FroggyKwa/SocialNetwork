from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.MainFeed.as_view(), name="main_feed"),
    path("news/following_posts", views.FriendsFeed.as_view(), name="friends_feed"),
    path("login", views.LoginView.as_view(), name="login_view"),
    path("signup", views.SignUpView.as_view(), name="signup_view"),
    path("post_upload", views.PostUploadView.as_view(), name="upload_post"),
    path(
        "post/<post_id>",
        login_required(
            views.PostDetailView.as_view(), "redirect_to", login_url="login_view"
        ),
        name="post_detail",
    ),
    path(
        "users/search/<username>",
        login_required(
            views.UserSearchView.as_view(), "redirect_to", login_url="login_view"
        ),
        name="users_search",
    ),
    path(
        "user/<username>",
        login_required(
            views.ProfilePageView.as_view(), "redirect_to", login_url="login_view"
        ),
        name="profile_page",
    ),
    path(
        "profile_update",
        login_required(
            views.ProfileUpdateView.as_view(), "redirect_to", login_url="login_view"
        ),
        name="profile_update",
    ),
    path(
        "user/<username>/subscribers",
        login_required(
            views.SubscribersListView.as_view(), "redirect_to", login_url="login_view"
        ),
        name="get_subscribers",
    ),
    path(
        "user/<username>/subscriptions",
        login_required(
            views.SubscriptionsListView.as_view(), "redirect_to", login_url="login_view"
        ),
        name="get_subscriptions",
    ),
]
