from django import forms
from django.contrib.auth.models import User

from social_network.models import Post


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field_name in ["username", "password", "confirm_password"]:
            self.fields[field_name].help_text = None

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class PostUploadForm(forms.ModelForm):
    name = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea)
    picture_url = forms.ImageField(required=False, label="Select an image")
    help_text = "Minimum resolution 500x500."

    class Meta:
        model = Post
        fields = ("name", "description", "picture_url")
