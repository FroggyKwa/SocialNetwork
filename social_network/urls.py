from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login", views.LoginView.as_view(), name="login_view"),
    path("signup", views.SignUpView.as_view(), name="signup_view"),
]
