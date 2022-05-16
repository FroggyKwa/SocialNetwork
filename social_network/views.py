import requests
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from social_network.forms import LoginForm, SignUpForm


class IndexView(LoginRequiredMixin, View):
    login_url = "login_view"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        return render(request, "base.html")


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            post_data = {
                "username": form.cleaned_data["username"],
                "password": form.cleaned_data["password"],
            }
            response = requests.post("http://localhost:8080/api/login", data=post_data)
            if response.status_code == 200:
                user = User.objects.get(id=response.json()["id"])
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                for error in response.json()["non_field_errors"]:
                    form.add_error(None, error)
        return render(request, "login.html", {"form": form, "errors": form.errors})


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            post_data = {
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password"],
            }
            response = requests.post("http://localhost:8080/api/signup", data=post_data)
            if response.status_code == 201:
                user = User.objects.get(id=response.json()["id"])
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                for error in response.json()["non_field_errors"]:
                    form.add_error(None, error)
        return render(request, "signup.html", {"form": form, "errors": form.errors})
