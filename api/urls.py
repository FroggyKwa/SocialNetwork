from django.urls import path

from . import views

urlpatterns = [
    path("login", views.LogInApiView.as_view(), name="api_log_in"),
    path("signup", views.SignUpAPIView.as_view(), name="api_sign_up"),
    path(
        r"user/<str:username>",
        views.UserRetrieveUpdateAPIView.as_view(),
        name="user_retrieve_and_update",
    ),
    path("upload_post", views.PostUploadView.as_view(), name="api_upload_post"),
    path("post_like", views.PostLikeAPIview.as_view(), name="post_like"),
    path("post_dislike", views.PostDisLikeAPIview.as_view(), name="post_dislike"),
    path("post_info", views.PostRetrieveUpdateAPIView.as_view(), name="post_info"),
    path("get_feed", views.GetUserFeedAPIView.as_view(), name="get_feed"),
    path(
        "query_by_username",
        views.GetUsersQueryByUsernameAPIView.as_view(),
        name="get_query",
    ),
]
