import requests
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from social_network.forms import LoginForm, SignUpForm, PostUploadForm
from social_network.models import Post


class IndexView(LoginRequiredMixin, View):
    login_url = "login_view"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        feed = requests.get("http://localhost:8080/api/get_feed", data={"user_id": request.user.id}).json()
        return render(request, "feed.html", context={"post": feed[0] if feed else None})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse("You are already authenticated.")
        form = LoginForm(request.POST)
        if form.is_valid():
            post_data = {
                "username": form.cleaned_data["username"],
                "password": form.cleaned_data["password"],
            }
            response = requests.post("http://localhost:8080/api/login", data=post_data)
            if response.status_code == 200:
                user = get_object_or_404(User, id=response.json()["id"])
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                for error in response.json()["non_field_errors"]:
                    form.add_error(None, error)
        return render(request, "login.html", {"form": form, "errors": form.errors})


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        form = SignUpForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse("You are already authenticated.")
        form = SignUpForm(request.POST)
        if form.is_valid():
            post_data = {
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password"],
            }
            response = requests.post("http://localhost:8080/api/signup", data=post_data)
            if response.status_code == 201:
                user = get_object_or_404(User, id=response.json()["id"])
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                for error in response.json()["non_field_errors"]:
                    form.add_error(None, error)
        return render(request, "signup.html", {"form": form, "errors": form.errors})


class PostUploadView(View, LoginRequiredMixin):
    login_url = "login_view"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        form = PostUploadForm()
        return render(request, "post_upload.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = PostUploadForm(request.POST)
        if form.is_valid():
            post_data = {
                "author_id": request.user.id,
                "name": form.cleaned_data["name"],
                "description": form.cleaned_data["description"],
            }
            response = requests.post(
                "http://localhost:8080/api/upload_post",
                data=post_data,
                files={"picture_url": request.FILES["picture_url"]},
            )
            if response.status_code == 201:
                return render(request, "post_success.html")
            else:
                for error in response.json()["non_field_errors"]:
                    form.add_error(None, error)
        return render(
            request, "post_upload.html", {"form": form, "errors": form.errors}
        )


class PostDetailView(View, LoginRequiredMixin):
    login_url = "login_view"
    redirect_field_name = "redirect_to"

    def get(self, request, post_id, *args, **kwargs):
        return render(
            request,
            "post_detail.html",
            context={"post": get_object_or_404(Post, pk=post_id)},
        )
