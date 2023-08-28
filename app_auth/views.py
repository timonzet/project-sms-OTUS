from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.views import (
    LoginView as LoginViewGeneric,
    LogoutView as LogoutViewGeneric,
)
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from my_app.models import ProfileUser
from my_app.views import ShowProfile
from .forms import AuthenticationForm, UserCreationForm
from django.db.models.signals import (
    post_save,
)  # Import a post_save signal when a user is created
from django.contrib.auth.models import (
    User,
)  # Import the built-in User model, which is a sender
from django.dispatch import receiver  # Import the receiver


class LoginView(LoginViewGeneric):
    template_name = "app_auth/login.html"
    form_class = AuthenticationForm

    next_page = reverse_lazy(
        "my_app:profile",
    )


class LogoutView(LogoutViewGeneric):
    next_page = reverse_lazy("app_auth:about-me")


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "app_auth/register.html"
    success_url = reverse_lazy("my_app:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user: AbstractUser = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            ProfileUser.objects.create(user=instance)


def validate_username(request):
    """Проверка доступности логина"""
    username = request.GET.get("username", None)
    response = {"is_taken": User.objects.filter(username__iexact=username).exists()}
    return JsonResponse(response)
