from django.urls import path

from . import views

urlpatterns = [
    path("post", views.PostUploadView.as_view(), name="upload_post"),
    path("login", views.LogInApiView.as_view(), name="log_in"),
    path("signup", views.SignUpAPIView.as_view(), name="sign_up"),
    path(r'user/<str:username>', views.UserRetrieveUpdateAPIView.as_view(), name="user_retrieve_and_update")
]
