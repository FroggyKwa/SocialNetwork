from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

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
    description = forms.CharField(widget=forms.Textarea, required=False)
    picture_url = forms.ImageField(label="Select an image")
    help_text = "Minimum resolution 500x500."

    class Meta:
        model = Post
        fields = ("name", "description", "picture_url")

    def clean_picture_url(self):
        image = self.cleaned_data.get("picture_url")
        width, height = get_image_dimensions(image)
        if image:
            if height < 500 or width < 500:
                raise ValidationError("Height and Width have to be more than 500px.")
            return image
        else:
            raise ValidationError("No image found")


class ProfileUpdateForm(forms.Form):
    email = forms.EmailField(required=False)
    username = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    age = forms.IntegerField(max_value=128, min_value=1, required=False)
    phone = forms.CharField(max_length=15, required=False)
    bio = forms.CharField(max_length=500, required=False, widget=forms.Textarea)
    is_hidden = forms.BooleanField(required=False, label="Hide liked")
    avatar = forms.ImageField(required=False)
